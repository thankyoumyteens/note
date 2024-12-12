# 订阅 topic

```java
// 订阅topic
consumer.subscribe(List.of("topic2"));
while (true) {
    // 拉取数据, 最大阻塞时间1秒
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
    for (ConsumerRecord<String, String> record : records) {
        System.out.println("topic = " + record.topic() +
                ", partition = " + record.partition() +
                ", offset = " + record.offset() +
                ", key = " + record.key() +
                ", value = " + record.value());
    }
}
```
