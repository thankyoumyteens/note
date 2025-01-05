# 安装 zookeeper

### 1. 下载

```sh
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.9.3/apache-zookeeper-3.9.3-bin.tar.gz
tar -zxvf apache-zookeeper-3.9.3-bin.tar.gz
mv apache-zookeeper-3.9.3-bin zk
```

### 2. 创建节点

```sh
sudo mkdir /zk
sudo chmod -R 777 /zk
# 创建三个文件夹, 代表三个服务器
mkdir -p /zk/server1 /zk/server2 /zk/server3
# 数据目录
mkdir -p /zk/data1 /zk/data2 /zk/data3
# 日志目录
mkdir -p /zk/log1 /zk/log2 /zk/log3
# 为每个节点创建 myid
echo "1" > /zk/data1/myid
echo "2" > /zk/data2/myid
echo "3" > /zk/data3/myid
```

### 3. 编辑配置文件

```sh
cd zk/conf/
cp zoo_sample.cfg zoo.cfg
vim zoo.cfg
```

编辑 zoo.cfg

```conf
# 每个节拍间隔多少毫秒
tickTime=2000
# 节点的初始化时间(单位: 节拍)
# 从节点启动并完成与主节点数据同步的时间
initLimit=10
# 心跳最大延迟时间(单位: 节拍)
# 用于主节点和从节点之间的心跳检测
syncLimit=5
# 数据目录
dataDir=/zk/data1
# 日志目录
dataLogDir=/zk/log1
# 客户端连接zookeeper的端口号
clientPort=2181
# 集群中的所有节点
# server配置项用于指定集群中的服务器信息
# 格式为server.<id>=<hostname>:<port1>:<port2>
# 其中<id>是服务器的唯一标识
# <hostname>是每个节点的主机名或IP地址
# <port1>是用于集群内节点间数据同步的端口
# <port2>是用于选举的端口
server.1=127.0.0.1:2888:3888
server.2=127.0.0.1:2889:3889
server.3=127.0.0.1:2890:3890
```

将 zookeeper 程序复制到几个 server 中:

```sh
cd ../../
cp -r zk/ /zk/server1/
cp -r zk/ /zk/server2/
cp -r zk/ /zk/server3/
```

编辑 server2 的 zoo.cfg:

```conf
# vim /zk/server2/zk/conf/zoo.cfg
# 修改下面配置
dataDir=/zk/data2
dataLogDir=/zk/log2
clientPort=2182
```

编辑 server3 的 zoo.cfg:

```conf
# vim /zk/server3/zk/conf/zoo.cfg
# 修改下面配置
dataDir=/zk/data3
dataLogDir=/zk/log3
clientPort=2183
```

### 4. 启动

```sh
/zk/server1/zk/bin/zkServer.sh start
/zk/server2/zk/bin/zkServer.sh start
/zk/server3/zk/bin/zkServer.sh start
```

### 5. 查看服务状态

```sh
/zk/server1/zk/bin/zkServer.sh status
/zk/server2/zk/bin/zkServer.sh status
/zk/server3/zk/bin/zkServer.sh status
```

### 6. 连接 zookeeper

```sh
/zk/server1/zk/bin/zkCli.sh -server 127.0.0.1:2181
```
