# Redis读写分离

就是主从复制，主机数据更新后根据配置和策略，自动同步到备机

# 配置读写分离

主从复制的开启，完全是在从节点发起的, 不需要在主节点做任何事情。

## 在从节点配置

从 5.0.0 版本开始，Redis 正式将 slaveof 命令改名成了 replicaof 命令并逐渐废弃原来的 slaveof 命令。

```conf
# replicaof 主节点的ip 主节点的端口号
replicaof 127.0.0.1 6379

masterauth 主节点的密码
# 默认yes 表示从节点只读
replica-read-only yes
```

# 无磁盘化传输

在使用Redis主从复制的时候，数据传输是通过master节点启动一个进程生成RDB文件然后把这个文件通过网络传输给slave节点

磁盘化传输: Redis主进程创建一个编写RDB的新进程放入磁盘文件。稍后，文件由父进程传输进程以增量的方式传递给从进程

无磁盘化传输: master会创建一个新的进程生成RDB文件，并且通过socket传输给slave节点，不会经过磁盘

## 开启无磁盘化传输

```conf
# 默认no
repl-diskless-sync yes
```
