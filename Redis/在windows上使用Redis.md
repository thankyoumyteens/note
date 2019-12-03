# 在windows上部署使用Redis

## 下载Redis

在Redis的[官网下载页](http://redis.io/download)上有各种各样的版本, 我这次是在windows上部署的, 要去[GitHub](https://github.com/MSOpenTech/redis)上下载。直接解压, 在\bin\release 目录下有个压缩包, 这就是我们需要的

## 启动Redis

直接在上图的目录打开命令窗口, 运行：
```
redis-server redis.windows.conf
```
结果就悲剧了, 提示：
```
QForkMasterInit: system error caught. error code=0x000005af, message=VirtualAllocEx failed.: unknown error 
```
原因是内存分配的问题（如果你的电脑够强悍, 可能不会出问题）。解决方法有两个, 第一：启动的时候使用--maxmemory 命令限制Redis的内存：
```
redis-server redis.windows.conf --maxmemory 200m
```
第二种方法就是修改配置文件redis.windows.conf ：
```
maxmemory 209715200
```
注意单位是字节, 改完之后再运行redis-server redis.windows.conf 就可以启动了

但是问题又来了, 关闭cmd窗口就会关闭Redis, 难道服务器上要一直开着吗？这显然是不科学的, 下面看怎么在服务器上部署。

## 部署Redis

其实Redis是可以安装成windows服务的, 开机自启动, 命令如下：
```
redis-server --service-install redis.windows.conf
```
安装完之后, 就可看到Redis已经作为windows服务了

但是安装好之后, Redis并没有启动, 启动命令如下：
```
redis-server --service-start
```
停止命令：
```
redis-server --service-stop
```
还可以安装多个实例
```
redis-server --service-install –service-name redisService1 –port 10001
redis-server --service-start –service-name redisService1
redis-server --service-install –service-name redisService2 –port 10002
redis-server --service-start –service-name redisService2
redis-server --service-install –service-name redisService3 –port 10003
redis-server --service-start –service-name redisService3
```
卸载命令：
```
redis-server --service-uninstall
```
最后提示一下：2.8版本的不支持32位系统, 32位系统要去下载2.6版本的。2.6版本的无法像上面一样方便的部署, 它提供一个叫RedisWatcher的程序来运行redis server, Redis停止后会自动重启。
