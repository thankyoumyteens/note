# 点对点模式

1. 配置类

```java
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class PointConfig {

    /**
     * 点对点队列
     */
    @Bean
    Queue queue1() {
        return new Queue("my.queue1", true);
    }
}
```

2. 生产者

```java
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class PointProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String msg) {
        rabbitTemplate.convertAndSend("my.queue1", msg);
    }

}
```

3. 消费者

```java
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class PointConsumer {

    @RabbitListener(queues = "my.queue1")
    public void listen(String msg) {
        System.out.println("消费:" + msg);
    }
}
```

4. 发送消息

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PointController {

    @Autowired
    private PointProducer pointProducer;

    @RequestMapping("/test/point")
    public String send() {
        pointProducer.send("hello");
        return "发送成功";
    }
}
```
