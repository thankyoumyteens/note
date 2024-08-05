# 任务调度

使用 xxl-job

## xxl-job 的路由策略

- 第一个（First）：固定选择第一个机器执行任务，适用于固定分配的场景
- 最后一个（Last）：固定选择最后一个机器执行任务，同样适用于固定分配的场景
- 轮询（Round）：通过轮询的方式选择执行器，这是一个默认的策略，可以平均分配任务到每个执行器
- 随机（Random）：随机选择一个执行器执行任务，适用于执行器配置相同的场景
- 一致性哈希（ConsistentHash）：根据任务参数的哈希值选择执行器，可以在一定程度上保证相同参数的任务总是由同一个执行器执行，有利于任务的本地缓存
- 最不经常使用（LFU）：优先选择使用频率最低的执行器，以尝试平衡各个执行器的负载
- 最近最久未使用（LRU）：优先选择最久未使用的执行器，适用于希望所有执行器都有机会执行任务的场景
- 故障转移（FaultTolerant）：当任务在一台执行器上执行失败时，会自动转移到其他执行器重试
- 忙碌转移（Busyover）：如果选中的执行器忙碌，则自动转移到其他执行器执行
- 分片广播(ShardingBroadcast): 所有机器都执行一次任务, 同时系统自动传递分片参数

## xxl-job 执行失败的解决方案

- 路由策略设置为故障转移, 并设置失败重试次数
- 设置报警邮件

## xxl-job 执行大数据量的任务

路由策略设置为分片广播。

```java
@XxlJob("testJob")
public void testJob() {
    // 当前分片序号(从0开始)，执行器集群列表中当前执行器的序号
    int shardIndex = XxlJobHelper.getShardIndex();
    // 总分片数，执行器集群的总机器数量
    int shardTotal = XxlJobHelper.getShardTotal();

    // 要处理的数据
    List<MyData> list = getData();
    // 执行任务逻辑
    for (MyData data : list) {
        // 当前分片项需要处理的数据
        if (data.getId() % shardTotal == shardIndex) {
            System.out.println("Shard " + shardIndex + " is running: " + i);
        }
    }
}
```
