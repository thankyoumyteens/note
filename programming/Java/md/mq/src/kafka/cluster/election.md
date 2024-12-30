# Leader 选举

在每个分区中，有一个副本（Replica）会被选举为 Leader，其余的副本则为 Follower。Leader 副本负责处理该分区的所有读写请求。当生产者（Producer）发送消息到分区时，消息会被发送到 Leader 副本，Leader 副本会将消息追加到分区的日志（Log）中。消费者（Consumer）从分区读取消息时，也是从 Leader 副本获取消息。

Follower 副本的主要职责是从 Leader 副本同步消息，保持与 Leader 副本的数据一致。它们会定期向 Leader 副本发送请求，获取最新的消息日志，并将其更新到自己的日志中。Follower 副本处于被动地位，不会处理读写请求，但在 Leader 副本出现故障时，它们可以参与 Leader 选举，以替换出现故障的 Leader。

当分区的 Leader 副本出现故障（如服务器宕机、网络故障等）或者由于网络分区导致 Leader 副本不可达时，就会触发 Leader 选举。另外，在创建新的分区或者添加新的副本时，也可能会进行 Leader 选举。

Follower 分为两种:

1. ISR: Leader 会同步复制数据
2. 普通: Leader 会异步复制数据, 数据可能会丢失

选举新 Leader 时, 会优先从 ISR 中选举, ISR 中没有才会从普通 Follower 中选举。
