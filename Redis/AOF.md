# AOF

AOF (Append Only File) 是通过保存Redis服务器所执行的写命令来记录数据库状态。

# AOF 配置

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

# AOF 文件恢复

重启 Redis 之后就会进行 AOF 文件的载入。

# AOF的优缺点

## 优点

1. AOF 持久化的方法提供了多种的同步频率，即使使用默认的同步频率每秒同步一次，Redis 最多也就丢失 1 秒的数据而已。
2. AOF 文件使用 Redis 命令追加的形式来构造，因此，即使 Redis 只能向 AOF 文件写入命令的片断，使用 redis-check-aof 工具也很容易修正 AOF 文件。
3. AOF 文件的格式可读性较强，这也为使用者提供了更灵活的处理方式。例如，如果我们不小心错用了 FLUSHALL 命令，在重写还没进行时，我们可以手工将最后的 FLUSHALL 命令去掉，然后再使用 AOF 来恢复数据。

## 缺点

1. 对于具有相同数据的的 Redis，AOF 文件通常会比 RDF 文件体积更大。
2. 虽然 AOF 提供了多种同步的频率，默认情况下，每秒同步一次的频率也具有较高的性能。但在 Redis 的负载较高时，RDB 比 AOF 具好更好的性能保证。
3. RDB 使用快照的形式来持久化整个 Redis 数据，而 AOF 只是将每次执行的命令追加到 AOF 文件中，因此从理论上说，RDB 比 AOF 方式更健壮。官方文档也指出，AOF 的确也存在一些 BUG，这些 BUG 在 RDB 没有存在。
