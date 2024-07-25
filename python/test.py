import threading
from seq_uuid import seq_uuid

test_ids = {}
test_ids_lock = threading.Lock()

def test_id_add(id: str):
    global test_ids
    with test_ids_lock:
        if id in test_ids:
            test_ids[id] += 1
        else:
            test_ids[id] = 1

def test_seq_uuid():
    for i in range(1000):
        id = seq_uuid()
        # test_id_add(id)
        print(id)

def multi_test_seq_uuid():

    threads = []
    for i in range(1000):
        threads.append(threading.Thread(target=test_seq_uuid, name=f"th-{i}"))
    for thd in threads:
        thd.start()
    for thd in threads:
        thd.join()


    # global test_ids
    # print(f"total id: {len(test_ids)}")
    # for id, cnt in test_ids.items():
    #     if cnt > 1:
    #         print(f"repeat id: {id}, count: {cnt}")

    
def check_repeat_id():
    file = 'a.log'
    fp = open(file, "r", encoding='utf-8')
    ids = set()
    lineno = 0
    while True:
        lineno += 1
        print(f"line {lineno}")
        try:
            id = fp.readline()
            if not id:
                break
            if id in ids:
                print(f"repeat id: {id}")
            else:
                ids.add(id)
        except Exception as e:
            print(f"readline error: {e}")

def check_thread_id():
    file = 'a3.thread'
    fp = open(file, "r", encoding='utf-8')
    ids = set()
    lineno = 0
    while True:
        lineno += 1
        # print(f"line {lineno}")
        try:
            id = fp.readline()
            if id is None or len(id) <= 0:
                break
            ids.add(id)
        except Exception as e:
            print(f"readline error: {e}")
    
    print(f"id count: {len(ids)}")

# check_repeat_id()
multi_test_seq_uuid()
# test_seq_uuid()
# check_thread_id()

