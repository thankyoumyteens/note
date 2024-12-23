# 安装 kafka-zookeeper

### 1. 安装 zookeeper

略

### 2. 下载

```sh
wget https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
tar -zxvf kafka_2.13-3.9.0.tgz
```

### 3. 配置

```sh
vim kafka_2.13-3.9.0/config/server.properties
```

修改下面配置:

```sh
# 集群中每个节点的brokerId必须唯一
broker.id=0
# 改成实际的zookeeper地址
zookeeper.connect=localhost:2181
# 存储消息内容的路径
log.dirs=/tmp/kafka-logs
# 云服务器需要开放9092端口
advertised.listeners=PLAINTEXT://服务器的ip:9092
```

### 4. 启动

```sh
cd kafka_2.13-3.9.0
bin/kafka-server-start.sh -daemon config/server.properties
```

### 5. 验证

```sh
/zk/server1/zk/bin/zkCli.sh -server 127.0.0.1:2181
ls /brokers
# 输出: [ids, seqid, topics]
```
