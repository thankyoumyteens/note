# 使用 Kafka 之后日志不打印异常

在 Spring 项目中使用 Kafka 时, 在 kafka 的消费者中调用的 service 如果抛出异常, 不会输出到日志中。

可以通过实现 ErrorHandler 接口来处理异常: 

```java
@Service
public class MyErrorHandler implements ErrorHandler {
    @Override
    public void handle(Exception e, ConsumerRecord<?, ?> consumerRecord) {
        // 输出异常
        log.error("kafka消费异常:" + consumerRecord, e);
    }
}

@Configuration
public class KafkaConfig {
    @Bean
    public MyErrorHandler errorHandler() {
        return new MyErrorHandler();
    }
}
```
