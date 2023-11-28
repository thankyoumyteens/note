# POM文件

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
    <version>2.4.1.RELEASE</version>
</dependency>
```

# application.yml

```yaml
server:
  port: 8080

spring:
  application:
    name: kafka
  kafka:
    bootstrap-servers: 127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094 # kafka集群信息
    producer: # 生产者配置
      retries: 3 # 设置大于0的值, 则客户端会将发送失败的记录重新发送
      batch-size: 16384 #16K
      buffer-memory: 33554432 #32M
      acks: 1
      # 指定消息key和消息体的编解码方式
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
    consumer:
      group-id: zhTestGroup # 消费者组
      enable-auto-commit: false # 关闭自动提交
      auto-offset-reset: earliest # 当各分区下有已提交的offset时, 从提交的offset开始消费；无提交的offset时, 从头开始消费
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
    listener:
      # 当每一条记录被消费者监听器（ListenerConsumer）处理之后提交
      # RECORD
      # 当每一批poll()的数据被消费者监听器（ListenerConsumer）处理之后提交
      # BATCH
      # 当每一批poll()的数据被消费者监听器（ListenerConsumer）处理之后, 距离上次提交时间大于TIME时提交
      # TIME
      # 当每一批poll()的数据被消费者监听器（ListenerConsumer）处理之后, 被处理record数量大于等于COUNT时提交
      # COUNT
      # TIME |　COUNT　有一个条件满足时提交
      # COUNT_TIME
      # 当每一批poll()的数据被消费者监听器（ListenerConsumer）处理之后, 手动调用Acknowledgment.acknowledge()后提交
      # MANUAL
      # 手动调用Acknowledgment.acknowledge()后立即提交, 一般使用这种
      # MANUAL_IMMEDIATE
      ack-mode: manual_immediate
```

# 生产者

```java
@RestController
public class KafkaProducer {
    private final static String TOPIC_NAME = "zhTest"; //topic的名称

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    @RequestMapping("/send")
    public void send() {
        kafkaTemplate.send(TOPIC_NAME, "key", "test message send~");
    }
}
```

# 消费者

```java
@Component
public class KafkaConsumer {

    //kafka的监听器, topic为"zhTest", 消费者组为"zhTestGroup"
    @KafkaListener(topics = "zhTest", groupId = "zhTestGroup")
    public void listenZhugeGroup(ConsumerRecord<String, String> record, Acknowledgment ack) {
        String value = record.value();
        System.out.println(value);
        System.out.println(record);
        //手动提交offset
        ack.acknowledge();
    }
}
```
