# 安装 kafka-zookeeper

### 1. 安装 zookeeper

略

### 2. 下载

```sh
wget https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
tar -zxvf kafka_2.13-3.9.0.tgz
mv kafka_2.13-3.9.0 kafka
```

### 3. 配置

```sh
sudo mkdir /kafka
sudo chmod -R 777 /kafka
# 创建三个文件夹，代表三个服务器
mkdir -p /kafka/server1 /kafka/server2 /kafka/server3
# 日志目录
mkdir -p /kafka/log1 /kafka/log2 /kafka/log3

vim kafka/config/server.properties
```

修改下面配置:

```sh
# 集群中每个节点的brokerId必须唯一
broker.id=1
port=9092
# 服务器内部网络接口的地址，用来集群内部通信
listeners=PLAINTEXT://localhost:9092
# 可以被外部客户端访问的地址
# 云服务器需要开放9092端口
advertised.listeners=PLAINTEXT://服务器的ip:9092
# 存储消息内容的路径
log.dirs=/kafka/log1
# 改成实际的zookeeper地址
zookeeper.connect=localhost:2181,localhost:2182,localhost:2183
```

将 kafka 程序复制到几个 server 中:

```sh
cp -r kafka/ /kafka/server1/
cp -r kafka/ /kafka/server2/
cp -r kafka/ /kafka/server3/
```

编辑 server2 的 server.properties:

```conf
# vim /kafka/server2/kafka/config/server.properties
# 修改下面配置
broker.id=2
port=9093
listeners=PLAINTEXT://localhost:9093
advertised.listeners=PLAINTEXT://服务器的ip:9093
log.dirs=/kafka/log2
```

编辑 server3 的 server.properties:

```conf
# vim /kafka/server3/kafka/config/server.properties
# 修改下面配置
broker.id=3
port=9094
listeners=PLAINTEXT://localhost:9094
advertised.listeners=PLAINTEXT://服务器的ip:9094
log.dirs=/kafka/log3
```

### 4. 启动

```sh
/kafka/server1/kafka/bin/kafka-server-start.sh -daemon /kafka/server1/kafka/config/server.properties
/kafka/server2/kafka/bin/kafka-server-start.sh -daemon /kafka/server2/kafka/config/server.properties
/kafka/server3/kafka/bin/kafka-server-start.sh -daemon /kafka/server3/kafka/config/server.properties
```
