# 最多一次

如果消费者在处理一批消息期间崩溃，从上次成功提交的偏移量到崩溃时正在处理的消息将不会被重新处理。这实现了最多一次 (At Most Once) 的消息传递语义。这种配置虽然提高了吞吐量和降低了延迟，但也增加了消息丢失的风险。

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class AtMostOnceConsumer {

    public static void main(String[] args) {
        // 创建Kafka消费者配置属性
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "test-group");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        // 启用自动提交偏移量，并设置较短的提交间隔(例如1秒)
        props.put("enable.auto.commit", "true");
        props.put("auto.commit.interval.ms", "1000"); // 可根据需要调整

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

                    // 注意：我们不在此处手动提交偏移量，因为我们启用了自动提交
                }
            }
        }
    }
}
```
