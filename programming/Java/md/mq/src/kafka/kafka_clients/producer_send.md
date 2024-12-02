# 异步发送消息

```java
// 消息内容
// 参数: topic, partition, key, value
ProducerRecord<String, String> record1 = new ProducerRecord<>("topic2", 0, "key1", "value1");
// 参数: topic, key, value
ProducerRecord<String, String> record2 = new ProducerRecord<>("topic2", "key2", "value2");

// 发送消息
Future<RecordMetadata> result1 = producer.send(record1);
Future<RecordMetadata> result2 = producer.send(record2);
```
