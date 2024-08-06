# work 模式

与点对点模式一样, 只是消费者由单个变为多个。

1. 配置类

```java
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class WorkConfig {

    /**
     * work队列
     */
    @Bean
    Queue queue2() {
        return new Queue("my.queue2", true);
    }
}
```

2. 生产者

```java
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class WorkProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String msg) {
        rabbitTemplate.convertAndSend("my.queue2", msg);
    }
}
```

3. 消费者

```java
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class WorkConsumer {

    @RabbitListener(queues = "my.queue2")
    public void listen1(String msg) {
        System.out.println("消费者1:" + msg);
    }

    @RabbitListener(queues = "my.queue2")
    public void listen2(String msg) {
        System.out.println("消费者2:" + msg);
    }

    @RabbitListener(queues = "my.queue2")
    public void listen3(String msg) {
        System.out.println("消费者3:" + msg);
    }
}
```

4. 发送消息

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WorkController {

    @Autowired
    private WorkProducer workProducer;

    @RequestMapping("/test/work")
    public String send() {
        for (int i = 0; i < 10; i++) {
            workProducer.send("hello " + i);
        }
        return "发送成功";
    }
}
```
