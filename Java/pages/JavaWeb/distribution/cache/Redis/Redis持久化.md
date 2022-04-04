# RDB

RDB全称redis database，在指定的时间间隔内将内存中的数据集快照写入磁盘，也就是Snapshot快照，它恢复时 直接将快照文件读到内存里

## 触发RDB

RDB 有两种触发方式，分别是自动触发和手动触发。

## 自动触发

在 redis.conf 配置文件中

```conf
# 当时间到900秒(15分钟)时，如果Redis数据发生了至少1次变化，则保存快照
save 900 1
# 当时间到300秒(5分钟)时，如果Redis数据发生了至少10次变化，则保存快照
save 300 10
# 当时间到60秒(1分钟)时，如果Redis数据发生了至少10000次变化，则保存快照
save save 60 10000
# 默认值为yes。当启用了RDB且最后一次后台保存数据失败，Redis是否停止接收数据
stop-writes-on-bgsave-error yes
# 默认值是yes。对于存储到磁盘中的快照进行压缩存储。redis会采用LZF算法进行压缩
rdbcompression yes
# 默认值是yes。在存储快照后，redis使用CRC64算法来进行数据校验，但是这样做会增加大约10%的性能消耗
rdbchecksum yes
# 设置快照的文件名，默认是 dump.rdb
dbfilename dump.rdb
# 设置快照文件的存放路径。默认是和当前配置文件保存在同一目录
dir /home/redis/rdb
```

## 手动触发

手动触发Redis进行RDB持久化的命令有两种：

- save：该命令会阻塞当前Redis服务器，执行save命令期间，Redis不能处理其他命令，直到RDB过程完成为止。
- bgsave：执行该命令时，Redis会在后台异步进行快照操作，快照同时还可以响应客户端请求。

基本上 Redis 内部所有的RDB操作都是采用 bgsave 命令。

## 恢复数据

将备份文件 (dump.rdb) 移动到 redis 安装目录并启动服务即可，redis就会自动加载文件数据至内存了。Redis 服务器在载入 RDB 文件期间，会一直处于阻塞状态，直到载入工作完成为止。

## 停用 RDB 持久化

在配置文件 redis.conf 中，可以注释掉所有的 save 行来停用保存功能或者改成`save ""`来实现停用

# AOF

AOF (Append Only File) 是通过保存Redis服务器所执行的写命令来记录数据库状态。

## AOF 配置

redis.conf 配置文件

```conf
# 默认值为no, 也就是说redis 默认使用的是rdb方式持久化
# 如果想要开启 AOF 持久化方式, 需要将 appendonly 修改为 yes
appendonly no
# aof文件名, 默认是"appendonly.aof"
appendfilename appendonly.aof
# aof持久化策略的配置
# no表示不执行fsync, 由操作系统保证数据同步到磁盘, 速度最快, 但是不太安全
# always表示每次写入都执行fsync, 以保证数据同步到磁盘, 效率很低
# everysec表示每秒执行一次fsync, 可能会导致丢失这1s数据。通常选择 everysec, 兼顾安全性和效率
appendfsync no

# 设置AOF文件的存放路径。默认是和当前配置文件保存在同一目录
dir /home/redis/rdb
```

## AOF 文件恢复

重启 Redis 之后就会进行 AOF 文件的载入。

# RDB和AOF对比

## RDB（Redis Database）

用指定的时间间隔对数据进行快照存储。

- 优点：因为是数据快照，所以生成的文件内容紧凑占用磁盘空间小，重启恢复到内存速度也较快，持久化的频率一般也会配置得比较低，并且执行过程交给子进程，对服务性能影响小。
- 缺点：数据安全性低，RDB是间隔一段时间进行持久化，如果持久化之间Redis发生故障，会发生数据丢失。所以这种方式更适合数据要求不严谨的时候

## AOF（Append Only File）

每一个收到的写命令都追加到文件中。

- 优点：因为追加写指令执行的频率高、间隔短，所以间隔期内进程停止丢失的数据较少，数据比较完整。
- 缺点：AOF文件比RDB文件大，且恢复速度慢。数据集大的时候，比RDB启动效率低。
