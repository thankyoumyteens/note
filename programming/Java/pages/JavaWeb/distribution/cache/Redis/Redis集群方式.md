# Redis主从模式

主机数据更新后根据配置和策略, 自动同步到备机。

开启主从复制, 是在从节点发起的, 不需要在主节点做任何事情。

## 在从节点配置

从 5.0.0 版本开始, Redis 正式将 slaveof 命令改名成了 replicaof 命令并逐渐废弃原来的 slaveof 命令。

```conf
# replicaof 主节点的ip 主节点的端口号
replicaof 127.0.0.1 6379
# 主节点的密码
masterauth 123456
# 默认yes 表示从节点只读
replica-read-only yes
```

## 开启无磁盘化传输

在使用Redis主从复制的时候, 数据传输是通过master节点启动一个进程生成RDB文件然后把这个文件通过网络传输给slave节点

磁盘化传输: Redis主进程创建一个编写RDB的新进程放入磁盘文件。稍后, 文件由父进程传输进程以增量的方式传递给从进程

无磁盘化传输: master会创建一个新的进程生成RDB文件, 并且通过socket传输给slave节点, 不会经过磁盘

```conf
# 默认no
repl-diskless-sync yes
```

# Redis哨兵

在主从模式上添加了一个哨兵的角色来监控集群的运行状态。

哨兵（Sentinel）是一个独立的进程。哨兵通过发送命令, 等待Redis服务器响应, 从而监控运行的多个Redis实例, 当哨兵监测到master不可用时, 会自动将slave切换成master, 然后通知其他的slave, 修改配置文件, 让它们切换master。当原来的master恢复后, 会变为slave。

## 配置哨兵

redis.conf
```conf
# 禁止保护模式, 使外部网络可以直接访问
protected-mode no
```

sentinel.conf
```conf
# 设置sentinel 的端口
port 26379
# 监控master
# mymaster代表master的别名, 可以自定义
# 192.168.11.128代表master的ip
# 6379代表master的端口
# 2代表只有当两个或两个以上的哨兵认为主服务器不可用的时候, 才会切换master
sentinel monitor mymaster 192.168.11.128 6379 2
# 配置master的访问密码
# mymaster是master的别名
# 123456是master的密码
sentinel auth-pass mymaster 123456
```

启动哨兵
```
redis-sentinel sentinel.conf
```

# Redis-Cluster

Redis-Cluster采用无中心结构, 每个节点保存数据和整个集群状态, 每个节点都和其他所有节点连接。

Redis集群预分好16384个slot, 当需要在 Redis 集群中放置一个 key-value 时, 根据 CRC16(key) mod 16384的值, 决定将一个key放到哪个slot中。

## Redis cluster搭建

redis.conf

```conf
daemonize yes # 后台启动
port 9001 # 节点的端口号
cluster-enabled yes # 启动集群模式
cluster-config-file nodes9001.conf # 节点配置文件
cluster-node-timeout 15000
appendonly yes #开启aof
bind 192.168.119.131 # 绑定当前机器IP, 可以是0.0.0.0
dir /usr/local/redis-cluster/9001/data/ # 数据文件存放位置
pidfile /var/run/redis_9001.pid # pid文件存放位置
```

启动所有的redis节点

## Redis旧版启动方式

复制redis解压目录src下的redis-trib.rb文件到自己的目录
```
cp /usr/local/redis/redis-3.2.0/src/redis-trib.rb ./
```

安装ruby环境
```
yum install ruby  
yum install rubygems
```

安装redis-trib.rb运行依赖的ruby的包redis-3.2.2.gem（对应版本最好跟redis一致）
```
wget https://rubygems.org/downloads/redis-3.2.2.gem
gem install -l ./redis-3.2.2.gem
```

使用redis-trib.rb创建集群
```
./redis-trib.rb create --replicas 1 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006
```

`--replicas 1` 参数表示为每个主节点创建一个从节点, 其他参数是实例的地址集合

## Redis5.0启动方式

Redis Cluster在5.0之后取消了ruby脚本redis-trib.rb的支持, 集合到redis-cli里, 避免了再安装ruby的相关环境。

```
redis-cli --cluster create 47.235.228.98:9001 47.235.228.98:9002 47.235.228.98:9003 47.235.228.98:9004 47.235.228.98:9005 47.235.228.98:9006
```

## 验证

```
# 连接其中一个redis结点
redis-cli -c -h 47.235.228.98 -p 9001
# 判断是否在集群中
cluster nodes
```
