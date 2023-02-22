# 使用客户端命令操作zookeeper

1、使用 ls 命令来查看当前 ZooKeeper 中所包含的内容
```
[zk: localhost:2181(CONNECTED) 1] ls /
[dubbo, default, zookeeper]
[zk: localhost:2181(CONNECTED) 2] 
```
2、创建一个新的 znode ，使用 create /zkPro myData
```
[zk: localhost:2181(CONNECTED) 2] create /zkPro myData
Created /zkPro
[zk: localhost:2181(CONNECTED) 3] 
```
3、再次使用 ls 命令来查看现在 zookeeper 中所包含的内容：
```
[zk: localhost:2181(CONNECTED) 3] ls /
[dubbo, default, zookeeper, zkPro]
[zk: localhost:2181(CONNECTED) 4] 
```
4、下面我们运行 get 命令来确认第二步中所创建的 znode 是否包含我们所创建的字符串：
```
[zk: localhost:2181(CONNECTED) 6] get /zkPro      
myData
cZxid = 0x1146
ctime = Tue Sep 04 10:40:49 CST 2018
mZxid = 0x1146
mtime = Tue Sep 04 10:40:49 CST 2018
pZxid = 0x1146
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 6
numChildren = 0
[zk: localhost:2181(CONNECTED) 7] 
```
5、下面我们通过 set 命令来对 zk 所关联的字符串进行设置：
```
[zk: localhost:2181(CONNECTED) 7] set /zkPro myData123456
cZxid = 0x1146
ctime = Tue Sep 04 10:40:49 CST 2018
mZxid = 0x1147
mtime = Tue Sep 04 10:43:59 CST 2018
pZxid = 0x1146
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 12
numChildren = 0
[zk: localhost:2181(CONNECTED) 8]
```
6、下面我们将刚才创建的 znode 删除
```
[zk: localhost:2181(CONNECTED) 8] delete /zkPro
[zk: localhost:2181(CONNECTED) 9] 
```
