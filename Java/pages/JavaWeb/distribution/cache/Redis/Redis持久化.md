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

### save

该命令会阻塞当前Redis服务器，执行save命令期间，Redis不能处理其他命令，直到RDB过程完成为止。

### bgsave

执行该命令时，Redis会在后台异步进行快照操作，快照同时还可以响应客户端请求。

具体操作是Redis进程执行fork操作创建子进程，RDB持久化过程由子进程负责，完成后自动结束。

阻塞只发生在fork阶段，一般时间很短。

基本上 Redis 内部所有的RDB操作都是采用 bgsave 命令。

## 恢复数据

将备份文件 (dump.rdb) 移动到 redis 安装目录并启动服务即可，redis就会自动加载文件数据至内存了。Redis 服务器在载入 RDB 文件期间，会一直处于阻塞状态，直到载入工作完成为止。

## 停止 RDB 持久化

在配置文件 redis.conf 中，可以注释掉所有的 save 行来停用保存功能或者改成`save ""`来实现停用

## RDB 的优势和劣势

### 优势

1. RDB是一个非常紧凑(compact)的文件，它保存了redis 在某个时间点上的数据集。这种文件非常适合用于进行备份和灾难恢复。
2. 生成RDB文件的时候，redis主进程会fork()一个子进程来处理所有保存工作，主进程不需要进行任何磁盘IO操作。
3. RDB 在恢复大数据集时的速度比 AOF 的恢复速度要快。

### 劣势

1. RDB方式数据没办法做到实时持久化/秒级持久化。因为bgsave每次运行都要执行fork操作创建子进程，属于重量级操作，如果不采用压缩算法(内存中的数据被克隆了一份，大致2倍的膨胀性需要考虑)，频繁执行成本过高(影响性能)
2. RDB文件使用特定二进制格式保存，Redis版本演进过程中有多个格式的RDB版本，存在老版本Redis服务无法兼容新版RDB格式的问题(版本不兼容)
3. 在一定间隔时间做一次备份，所以如果redis意外down掉的话，就会丢失最后一次快照后的所有修改(数据有丢失)


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

## AOF的优缺点

### 优点

1. AOF 持久化的方法提供了多种的同步频率，即使使用默认的同步频率每秒同步一次，Redis 最多也就丢失 1 秒的数据而已。
2. AOF 文件使用 Redis 命令追加的形式来构造，因此，即使 Redis 只能向 AOF 文件写入命令的片断，使用 redis-check-aof 工具也很容易修正 AOF 文件。
3. AOF 文件的格式可读性较强，这也为使用者提供了更灵活的处理方式。例如，如果我们不小心错用了 FLUSHALL 命令，在重写还没进行时，我们可以手工将最后的 FLUSHALL 命令去掉，然后再使用 AOF 来恢复数据。

### 缺点

1. 对于具有相同数据的的 Redis，AOF 文件通常会比 RDF 文件体积更大。
2. 虽然 AOF 提供了多种同步的频率，默认情况下，每秒同步一次的频率也具有较高的性能。但在 Redis 的负载较高时，RDB 比 AOF 具好更好的性能保证。
3. RDB 使用快照的形式来持久化整个 Redis 数据，而 AOF 只是将每次执行的命令追加到 AOF 文件中，因此从理论上说，RDB 比 AOF 方式更健壮。官方文档也指出，AOF 的确也存在一些 BUG，这些 BUG 在 RDB 没有存在。
