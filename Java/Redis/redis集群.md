# Redis-Cluster

redis最开始使用主从模式做集群，若master宕机需要手动配置slave转为master；后来为了高可用提出来哨兵模式，该模式下有一个哨兵监视master和slave，若master宕机可自动将slave转为master，但它也有一个问题，就是不能动态扩充；所以在3.x提出cluster集群模式。

Redis-Cluster采用无中心结构，每个节点保存数据和整个集群状态,每个节点都和其他所有节点连接。

Redis集群预分好16384个slot，当需要在 Redis 集群中放置一个 key-value 时，根据 CRC16(key) mod 16384的值，决定将一个key放到哪个slot中。

# Redis cluster集群搭建

## redis.conf

```conf
daemonize yes # 后台启动
port 9001 # 节点的端口号
cluster-enabled yes # 启动集群模式
cluster-config-file nodes9001.conf # 节点配置文件
cluster-node-timeout 15000
appendonly yes #开启aof
bind 192.168.119.131 # 绑定当前机器IP，可以是0.0.0.0
dir /usr/local/redis-cluster/9001/data/ # 数据文件存放位置
pidfile /var/run/redis_9001.pid # pid文件存放位置
```

启动所有的redis节点

## Redis5.0启动方式

Redis Cluster 在5.0之后取消了ruby脚本 redis-trib.rb的支持（手动命令行添加集群的方式不变），集合到redis-cli里，避免了再安装ruby的相关环境。

```
redis-cli --cluster create 47.235.228.98:9001 47.235.228.98:9002 47.235.228.98:9003 47.235.228.98:9004 47.235.228.98:9005 47.235.228.98:9006
```

### 验证

```
# 连接其中一个redis结点
redis-cli -c -h 47.235.228.98 -p 9001
# 判断是否在集群中
cluster nodes
```

## Redis旧版启动方式

### 安装redis-trib

复制redis解压文件src下的redis-trib.rb文件到自己的目录
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

### 使用redis-trib.rb创建集群

```
./redis-trib.rb create --replicas 1 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 127.0.0.1:7006
```
使用create命令 --replicas 1 参数表示为每个主节点创建一个从节点，其他参数是实例的地址集合
