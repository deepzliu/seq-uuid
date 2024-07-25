# seq-uuid

生成顺序UUID.

场景: 顺序存储, 如IM消息, 日志等

格式: ts+ms+seq+ip+thread_id, 各字节数: 4+3+2+4+3

性能: 100000个uuid, 用时8s, 即12w/s, 且无重复.
