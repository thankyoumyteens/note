# 高可用

1. 集群模式
2. 分区备份机制

kafka 的服务端由被称为 broker 的进程构成, 一个 kafka 集群由多个 broker 组成。

## 分区备份机制

一个 topic 有多个分区, 每个分区有多个副本, 其中有一个 leader, 其它的是 follower, 副本会存储在不同的 broker 中。所有的 follower 内容都是和 leader 相同的。如果 leader 发生故障, 会从 follower 中选举出新 leader。

follower 分为两种:

1. ISR: leader 会同步复制数据
2. 普通: leader 会异步复制数据, 数据可能会丢失

选举新 leader 时, 会优先从 ISR 中选举, ISA 中没有才会从普通 follower 中选举。
