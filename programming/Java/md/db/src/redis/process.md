# 慢查询

客户端请求执行流程

1. 客户端发送命令
2. redis 把收到的命令加入排队的队列
3. 执行排到的命令
4. 返回结果

慢查询发生在第 3 阶段, 客户端超时不一定是慢查询(4 个过程都可能导致超时)。

## slowlog

Slowlog 是 Redis 用来记录查询执行时间的日志系统。查询执行时间指的是不包括像客户端响应、发送回复等 IO 操作，而单单是执行一个查询命令所耗费的时间。

配置参数:

- `slowlog-log-slower-than` 决定要对执行时间大于多少微秒的操作进行记录
- `slowlog-max-len` 它决定 slowlog 最多能保存多少条日志。slowlog 本身是一个 FIFO 队列，当队列大小超过 slowlog-max-len 时，最旧的一条日志将被删除，而最新的一条日志加入到 slowlog 末尾

可以通过 redis.conf 文件进行配置:

```conf
slowlog-log-lower-than 1000
slowlog-max-len 200
```
