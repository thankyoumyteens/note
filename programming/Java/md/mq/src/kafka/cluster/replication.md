# Kafka 副本集

Kafka 副本集(Replication)是 Kafka 为了实现高可用性和数据冗余而采用的一种机制。

在 Kafka 集群中，一个主题(Topic)可以被划分为多个分区(Partition)，每个分区可以有多个副本(Replica)。这些副本分布在不同的代理节点(Broker)上，其中一个副本被指定为领导者(Leader)，其余的为追随者(Follower)。

例如，假设有一个名为 “my_topic” 的主题，它有 3 个分区(Partition 0、Partition 1、Partition 2)，每个分区有 3 个副本。那么在 Kafka 集群中，这些分区副本会分布在不同的代理节点上，形成一个副本集结构，用于确保数据的可靠性和可访问性。
