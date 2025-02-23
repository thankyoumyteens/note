# 主从复制

- 一个 master 可以有多个 slave
- 一个 slave 只能有一个 master
- 数据流向是单向的, 从 master 到 slave

## 通过配置文件实现主从复制

### 1. 主节点配置

主节点默认无需特殊配置。

### 2. 从节点配置

从节点需要明确指定主节点的地址和端口。编辑从节点的配置文件（redis.conf）：

```conf
# 绑定 IP 地址，0.0.0.0 表示监听所有网络接口
bind 0.0.0.0
# 设置 Redis 服务监听的端口号，这里设置为 6380
port 6380
# 是否以守护进程（后台）模式运行，yes 表示以守护进程模式运行
daemonize yes
# 指定 Redis 进程 ID 文件的路径，用于存储 Redis 服务的进程 ID
pidfile /var/run/redis_6380.pid
# 指定日志文件的路径，Redis 的运行日志将写入该文件
logfile /var/log/redis_6380.log
# 指定持久化数据文件的名称（RDB 文件）
dbfilename dump.rdb
# 指定持久化数据文件的存储目录
dir /var/lib/redis/6380

# 指定主节点
replicaof <主节点IP> <主节点端口>
# 例如：
# replicaof 127.0.0.1 6379

# 如果主节点有密码，需配置
masterauth <主节点密码>
```

### 3. 启动 Redis 实例

```sh
# 启动主节点
redis-server /path/to/redis_6379.conf
# 启动从节点
redis-server /path/to/redis_6380.conf
```

### 4. 验证

```sh
# 连接到主节点
redis-cli -h 127.0.0.1 -p 6379
# 执行命令查看复制信息
info replication
# 输出示例
# Replication
role:master
connected_slaves:1
slave0:ip=127.0.0.1,port=6380,state=online,offset=12345,lag=0
```

## 通过 Redis 命令行动态配置实现主从复制

### 1. 在从节点上执行

```sh
# 连接从节点
redis-cli -h 127.0.0.1 -p 6380

# 设置主节点
REPLICAOF <主节点IP> <主节点端口>
# 例如：
# REPLICAOF 127.0.0.1 6379

# 如果主节点有密码，设置密码
CONFIG SET masterauth <主节点密码>
```

### 2. 测试数据同步

```sh
# 在主节点写入数据
SET key1 value1

# 在从节点读取数据
GET key1
```

如果返回 value1，说明主从复制配置成功
