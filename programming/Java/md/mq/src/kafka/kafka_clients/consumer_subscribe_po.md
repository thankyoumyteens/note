# 从指定的 offset 开始消费

```java
Consumer<String, String> consumer = new KafkaConsumer<>(properties);

TopicPartition partition0 = new TopicPartition("topic2", 0);
consumer.assign(List.of(partition0));
while (true) {
    // 从头开始消费partition 0
    consumer.seek(partition0, 0);

    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
    Set<TopicPartition> partitions = records.partitions();
    Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
    for (TopicPartition partition : partitions) {
        List<ConsumerRecord<String, String>> recordsInPartition = records.records(partition);
        for (ConsumerRecord<String, String> record : recordsInPartition) {
            System.out.println("topic = " + record.topic() +
                    ", partition = " + record.partition() +
                    ", offset = " + record.offset() +
                    ", key = " + record.key() +
                    ", value = " + record.value());
        }
        long lastOffset = recordsInPartition.get(recordsInPartition.size() - 1).offset();
        offsets.put(partition, new OffsetAndMetadata(lastOffset + 1));
    }
    consumer.commitSync(offsets);
}
```
