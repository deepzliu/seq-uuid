import threading
from datetime import datetime
import socket

local_ip_str: str
local_ip: int = 0
def get_local_ip():
    global local_ip_str, local_ip
    if local_ip > 0:
        return local_ip_str, local_ip
    
    # 获取本机所有 IP 地址
    hostname = socket.gethostname()
    ip_list = set()
    # 获取IP地址信息
    addr_infos = socket.getaddrinfo(hostname, None)
    
    for addr in addr_infos:
        ip_list.add(addr[4][0])

    for ip in ip_list:
        values = ip.split(".")
        if len(values) == 4 and int(values[3]) > 1 and int(values[3]) < 255:
            ip_int = (int(values[0]) << 24) | (int(values[1]) << 16) | (int(values[2]) << 8) | int(values[3])
            # print("found ip: %s, %032x" % (ip, ip_int))
            local_ip_str = ip
            local_ip = ip_int
            return ip, ip_int
    return "", 0

uuid_seq: int = 0
seq_lock = threading.Lock()
def seq_incr():
    seq = 0
    with seq_lock:
        global uuid_seq
        uuid_seq += 1
        uuid_seq %= 0xffff
        seq = uuid_seq
    return seq

def seq_uuid():

    # format: "ts+ms+seq+ip+thread_id"
    # size: "4+3+2+4+3"
    # uuid demo: "d35866e9-bdca-40ec-abeb-1ea0b11fc7f8"
    # uuid size: "4+2+2+2+6"
    
    curr_time = datetime.now()
    ts = int(curr_time.timestamp())
    ms = curr_time.microsecond
    seq = seq_incr()
    ip, ip_int = get_local_ip()
    thread_id = threading.get_native_id()

    values = bytearray(16)

    values[0] = (ts & 0xff000000) >> 24
    values[1] = (ts & 0x00ff0000) >> 16
    values[2] = (ts & 0x0000ff00) >> 8
    values[3] = (ts & 0x000000ff)

    values[4] = (ms & 0xff0000) >> 16
    values[5] = (ms & 0x00ff00) >> 8
    values[6] = (ms & 0x0000ff)

    values[7] = (seq & 0xff00) >> 8
    values[8] = (seq & 0xff)

    values[9]  = (ip_int & 0xff000000) >> 24
    values[10] = (ip_int & 0x00ff0000) >> 16
    values[11] = (ip_int & 0x0000ff00) >> 8
    values[12] = (ip_int & 0x000000ff)

    values[13] = (thread_id & 0xff0000) >> 16
    values[14] = (thread_id & 0x00ff00) >> 8
    values[15] = (thread_id & 0xff)

    id = '%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x' % (
                values[0], 
                values[1],
                values[2],
                values[3],
                values[4],
                values[5],
                values[6],
                values[7],
                values[8],
                values[9],
                values[10],
                values[11],
                values[12],
                values[13],
                values[14],
                values[15],
            )

    return id

