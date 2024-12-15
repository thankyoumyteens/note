# 订阅 topic 和 partition

```java
consumer.subscribe(List.of("topic2"));
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
    // 获取所有分区
    Set<TopicPartition> partitions = records.partitions();
    // 记录每个分区的offset, 用于提交
    Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();

    for (TopicPartition partition : partitions) {
        // 获取指定分区的消息
        List<ConsumerRecord<String, String>> recordsInPartition = records.records(partition);
        for (ConsumerRecord<String, String> record : recordsInPartition) {
            System.out.println("topic = " + record.topic() +
                    ", partition = " + record.partition() +
                    ", offset = " + record.offset() +
                    ", key = " + record.key() +
                    ", value = " + record.value());
        }
        // 获取最后一条消息的offset
        long lastOffset = recordsInPartition.get(recordsInPartition.size() - 1).offset();
        // 记录offset
        offsets.put(partition, new OffsetAndMetadata(lastOffset + 1));
    }

    // 手动提交offset
    consumer.commitSync(offsets);
}
```
