# 增加 partition

```java
Map<String, NewPartitions> newPartitions = new HashMap<>();
// 把partition增加到3个
NewPartitions newPartition = NewPartitions.increaseTo(3);
newPartitions.put("topic2", newPartition);
adminClient.createPartitions(newPartitions);
```
