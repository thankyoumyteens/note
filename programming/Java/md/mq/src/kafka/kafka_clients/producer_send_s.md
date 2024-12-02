# 同步发送消息

```java
// 消息内容
ProducerRecord<String, String> record = new ProducerRecord<>("topic2", "key2", "value2");
// 发送消息
Future<RecordMetadata> result = producer.send(record);
// 阻塞等待消息发送成功
RecordMetadata recordMetadata = result.get();
// 打印分区和偏移量
System.out.println("partition: " + recordMetadata.partition() + ", offset: " + recordMetadata.offset());
```
