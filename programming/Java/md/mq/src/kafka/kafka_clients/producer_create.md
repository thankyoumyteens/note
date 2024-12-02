# 连接 kafka

```java
Properties properties = new Properties();
// kafka服务器地址
properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
// key value的序列化类
properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");

// 连接kafka
Producer<String, String> producer = new KafkaProducer<>(properties);

producer.close();
```
