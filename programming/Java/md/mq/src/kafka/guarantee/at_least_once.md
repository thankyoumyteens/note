# 至少一次

可以确保即使消费者在处理消息的过程中发生故障，也不会丢失任何消息，虽然有可能会导致一些消息被重复处理。

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class AtLeastOnceConsumer {

    public static void main(String[] args) {
        // 创建Kafka消费者配置属性
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "test-group");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        // 禁用自动提交偏移量
        props.put("enable.auto.commit", "false");

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

                    // 模拟消息处理完成后的操作
                    try {
                        // 假设处理需要一定时间
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }

                // 批量处理完所有消息后，同步提交偏移量
                consumer.commitSync(); // 同步提交确保所有之前的消息都已经被处理
            }
        }
    }
}
```
