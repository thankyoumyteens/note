# maven依赖

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
</dependency>
```

# 生产者的配置文件

```yaml
spring:
  #重要提示:kafka配置,该配置属性将直接注入到KafkaTemplate中
  kafka:
    bootstrap-servers: 10.200.8.29:9092,10.200.8.30:9092
    #https://kafka.apache.org/documentation/#producerconfigs
    producer:
      # 可重试错误的重试次数，例如“连接错误”、“无主且未选举出新Leader”
      retries: 1 #生产者发送消息失败重试次数
      # 多条消息放同一批次，达到多达就让Sender线程发送
      batch-size: 16384 # 同一批次内存大小（默认16K）
      # 发送消息的速度超过发送到服务器的速度，会导致空间不足。send方法要么被阻塞，要么抛异常
      # 取决于如何设置max.block.ms，表示抛出异常前可以阻塞一段时间
      buffer-memory: 314572800 #生产者内存缓存区大小(300M = 300*1024*1024)
      #acks=0:无论成功还是失败，只发送一次。无需确认
      #acks=1:即只需要确认leader收到消息
      #acks=all或-1:ISR + Leader都确定收到
      acks: 1
      key-serializer: org.apache.kafka.common.serialization.StringSerializer #key的编解码方法
      value-serializer: org.apache.kafka.common.serialization.StringSerializer #value的编解码方法
      #开启事务，但是要求ack为all，否则无法保证幂等性
      #transaction-id-prefix: "COLA_TX"
      #额外的，没有直接有properties对应的参数，将存放到下面这个Map对象中，一并初始化
      properties:
        #自定义拦截器，注意，这里结尾时classes(先于分区器，快递先贴了标签再指定地址)
        interceptor.classes: cn.com.controller.TimeInterceptor
        #自定义分区器
        #partitioner.class: com.alibaba.cola.kafka.test.customer.inteceptor.MyPartitioner
        #即使达不到batch-size设定的大小，只要超过这个毫秒的时间，一样会发送消息出去
        linger.ms: 1000
        #最大请求大小，200M = 200*1024*1024，与服务器broker的message.max.bytes最好匹配一致
        max.request.size: 209715200
        #Producer.send()方法的最大阻塞时间(115秒)
        # 发送消息的速度超过发送到服务器的速度，会导致空间不足。send方法要么被阻塞，要么抛异常
        # 取决于如何设置max.block.ms，表示抛出异常前可以阻塞一段时间
        max.block.ms: 115000
        #该配置控制客户端等待服务器的响应的最长时间。
        #如果超时之前仍未收到响应，则客户端将在必要时重新发送请求，如果重试次数（retries）已用尽，则会使请求失败。 
        #此值应大于replica.lag.time.max.ms（broker配置），以减少由于不必要的生产者重试而导致消息重复的可能性。
        request.timeout.ms: 115000
        #等待send回调的最大时间。常用语重试，如果一定要发送，retries则配Integer.MAX
        #如果超过该时间：TimeoutException: Expiring 1 record(s) .. has passed since batch creation
        delivery.timeout.ms: 120000
        # 生产者在服务器响应之前能发多少个消息，若对消息顺序有严格限制，需要配置为1
        # max.in.flight.requests.per.connection: 1
```

# Kafka生产者

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class KafkaProducer {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @GetMapping("/kafka/{message}")
    public void sendMessage1(@PathVariable("message") String normalMessage) {
        kafkaTemplate.send("topic1", normalMessage).addCallback(success -> {
            // 消息发送到的topic
            String topic = success.getRecordMetadata().topic();
            // 消息发送到的分区
            int partition = success.getRecordMetadata().partition();
            // 消息在分区内的offset
            long offset = success.getRecordMetadata().offset();
            System.out.println("发送消息成功:" + topic + "-" + partition + "-" + offset);
        }, failure -> {
            System.out.println("发送消息失败:" + failure.getMessage());
        });
    }
}
```

# 消费者的配置文件

```yaml
spring:
  kafka:
    bootstrap-servers: 10.200.8.29:9092,10.200.8.30:9092
    #https://kafka.apache.org/documentation/#consumerconfigs
    consumer:
      #消费方式: 在有提交记录的时候，earliest与latest是一样的，从提交记录的下一条开始消费
      # earliest：无提交记录，从头开始消费
      #latest：无提交记录，从最新的消息的下一条开始消费
      auto-offset-reset: earliest 
      enable-auto-commit: true #是否自动提交偏移量offset
      auto-commit-interval: 1S #前提是 enable-auto-commit=true。自动提交的频率
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      max-poll-records: 2
      properties:
      #如果在这个时间内没有收到心跳，该消费者会被踢出组并触发{组再平衡 rebalance}
      session.timeout.ms: 120000
      #最大消费时间。此决定了获取消息后提交偏移量的最大时间，超过设定的时间（默认5分钟），服务端也会认为该消费者失效。踢出并再  衡
      max.poll.interval.ms: 300000
      #配置控制客户端等待请求响应的最长时间。 
      #如果在超时之前没有收到响应，客户端将在必要时重新发送请求，
      #或者如果重试次数用尽，则请求失败。
      request.timeout.ms: 60000
      #订阅或分配主题时，允许自动创建主题。0.11之前，必须设置false
      allow.auto.create.topics: true
      #poll方法向协调器发送心跳的频率，为session.timeout.ms的三分之一
      heartbeat.interval.ms: 40000 
      #每个分区里返回的记录最多不超max.partitions.fetch.bytes 指定的字节
      #0.10.1版本后 如果 fetch 的第一个非空分区中的第一条消息大于这个限制
      #仍然会返回该消息，以确保消费者可以进行
      #max.partition.fetch.bytes=1048576  #1M
    listener:
      #当enable.auto.commit的值设置为false时，该值会生效；为true时不会生效
      #manual_immediate:需要手动调用Acknowledgment.acknowledge()后立即提交
      ack-mode: manual_immediate
      missing-topics-fatal: true #如果至少有一个topic不存在，true启动失败。false忽略
      #type: single #单条消费？批量消费？ #批量消费需要配合 consumer.max-poll-records
      type: batch
      concurrency: 2 #配置多少，就为为每个消费者实例创建多少个线程。多出分区的线程空闲
    template:
      default-topic: "COLA"
```

# Kafka消费者

```java
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.TopicPartition;
import org.springframework.stereotype.Component;

@Component
public class KafkaConsumer {

    @KafkaListener(
            id = "consumer1",
            groupId = "topic1-consumer",
            topicPartitions = {
                    @TopicPartition(topic = "topic1", partitions = {"0", "1", "2"}),
            })
    public void onMessage1(ConsumerRecord<?, ?> record) {
        // 消费的哪个topic、partition的消息,打印出消息内容
        System.out.println("简单消费：" + record.topic() + "-" + record.partition() + "-" + record.value());
    }
}
```
