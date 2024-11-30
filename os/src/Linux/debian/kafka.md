# kafka

### 1. 安装

```sh
wget https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
tar -zxvf kafka_2.13-3.9.0.tgz
```

### 2. 配置

```sh
# 云服务器需要开放9092端口
vim config/kraft/server.properties
# advertised.listeners=PLAINTEXT://服务器的ip:9092
```

### 3. 初始化

```sh
# 格式化 kraft 文件夹（新安装后只需执行一次）
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
```

### 4. 启动

```sh
# 启动
bin/kafka-server-start.sh -daemon config/kraft/server.properties
```
