# Zookeeper单机模式安装

配置JAVA环境

下载并解压zookeeper
```
cd /usr/local
wget http://mirror.bit.edu.cn/apache/zookeeper/stable/zookeeper-3.4.12.tar.gz
tar -zxvf zookeeper-3.4.12.tar.gz
cd zookeeper-3.4.12
```
重命名配置文件zoo_sample.cfg
```
cp conf/zoo_sample.cfg conf/zoo.cfg
```
启动zookeeper
```
bin/zkServer.sh start
```
- 启动命令: ./bin/zkServer.sh start
- 停止命令: ./bin/zkServer.sh stop
- 重启命令: ./bin/zkServer.sh restart
- 状态查看命令: ./bin/zkServer.sh status

检测是否成功启动, 用zookeeper客户端连接下服务端
```
./bin/zkCli.sh -server 127.0.0.1:2181
```

# Zookeeper集群模式安装

下载解压

重命名 zoo_sample.cfg文件
```
cp conf/zoo_sample.cfg conf/zoo.cfg
```
修改配置文件zoo.cfg
```
dataDir=/tmp/zookeeper
clientPort=2181
server.1=192.168.1.101:2888:3888
server.2=192.168.1.102:2888:3888
server.3=192.168.1.103:2888:3888
```
配置说明

- tickTime: 这个时间是作为 Zookeeper 服务器之间或客户端与服务器之间维持心跳的时间间隔, 也就是每个 tickTime 时间就会发送一个心跳。
- initLimit: 这个配置项是用来配置 Zookeeper 接受客户端（这里所说的客户端不是用户连接 Zookeeper 服务器的客户端, 而是 Zookeeper 服务器集群中连接到 Leader 的 Follower 服务器）初始化连接时最长能忍受多少个心跳时间间隔数。当已经超过 10个心跳的时间（也就是 tickTime）长度后 Zookeeper 服务器还没有收到客户端的返回信息, 那么表明这个客户端连接失败。总的时间长度就是 10*2000=20 秒
- syncLimit: 这个配置项标识 Leader 与 Follower 之间发送消息, 请求和应答时间长度, 最长不能超过多少个 tickTime 的时间长度, 总的时间长度就是 5*2000=10秒
- dataDir: 顾名思义就是 Zookeeper 保存数据的目录, 默认情况下, Zookeeper 将写数据的日志文件也保存在这个目录里。
- clientPort: 这个端口就是客户端连接 Zookeeper 服务器的端口, Zookeeper 会监听这个端口, 接受客户端的访问请求。
- server.A=B:C:D: 其中 A 是一个数字, 表示这个是第几号服务器；B 是这个服务器的 ip 地址；C 表示的是这个服务器与集群中的 Leader 服务器交换信息的端口；D 表示的是万一集群中的 Leader 服务器挂了, 需要一个端口来重新进行选举, 选出一个新的 Leader, 而这个端口就是用来执行选举时服务器相互通信的端口。

创建文件夹/tmp/zookeeper, 并创建文件myid文件, 写入当前实例的server id, 即1、2、3
```
cd /tmp/zookeeper
echo 1 > myid
```
启动三台机器上的zookeeper实例
```
bin/zkServer.sh start conf/zoo.cfg
```
检测集群状态
```
bin/zkServer.sh status conf/zoo.cfg
```
