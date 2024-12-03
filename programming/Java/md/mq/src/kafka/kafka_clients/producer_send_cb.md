# 异步发送消息回调

```java
// 消息内容
ProducerRecord<String, String> record = new ProducerRecord<>("topic2", "key2", "value2");
// 发送消息
producer.send(record, new Callback() {
    @Override
    public void onCompletion(RecordMetadata metadata, Exception exception) {
        if (exception == null) {
            System.out.println("消息发送成功");
            System.out.println("topic: " + metadata.topic());
            System.out.println("partition: " + metadata.partition());
            System.out.println("offset: " + metadata.offset());
        } else {
            System.out.println("消息发送失败");
        }
    }
});
```
