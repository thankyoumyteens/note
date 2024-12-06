# 精确一次

### 1. 生产者

```java
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class ExactlyOnceProducer {

    public static void main(String[] args) {
        // 创建Kafka生产者配置属性
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        // 启用幂等生产者
        props.put("enable.idempotence", "true");

        // 设置事务ID
        props.put("transactional.id", "my-transactional-id");

        // 创建Kafka生产者实例
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            // 初始化事务
            producer.initTransactions();

            try {
                // 开始一个新事务
                producer.beginTransaction();

                // 发送消息
                ProducerRecord<String, String> record = new ProducerRecord<>("your-topic-name", "key", "value");
                RecordMetadata metadata = producer.send(record).get(); // 阻塞等待发送完成

                // 如果需要发送更多消息，可以继续添加到当前事务中

                // 提交事务
                producer.commitTransaction();
                System.out.println("Transaction committed successfully.");
            } catch (ExecutionException | InterruptedException e) {
                // 如果发生异常，回滚事务
                producer.abortTransaction();
                System.err.println("Transaction aborted due to exception: " + e.getMessage());
            }
        }
    }
}
```

### 2. 消费者

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class ExactlyOnceConsumer {

    public static void main(String[] args) {
        // 创建Kafka消费者配置属性
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "test-group");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        // 禁用自动提交偏移量
        props.put("enable.auto.commit", "false");

        // 设置隔离级别为读已提交，以确保消费者只会看到成功提交的事务中的消息
        props.put("isolation.level", "read_committed");

        // 创建Kafka消费者实例
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            // 订阅主题
            consumer.subscribe(Collections.singletonList("your-topic-name"));

            // 持续轮询消息
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    // 处理消息
                    System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());

                    // 在这里添加你的业务逻辑以处理消息
                }

                // 批量处理完所有消息后，同步提交偏移量
                consumer.commitSync(); // 同步提交确保所有之前的消息都已经被处理
            }
        }
    }
}
```
