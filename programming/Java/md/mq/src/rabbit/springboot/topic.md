# Topic

1. 配置类, 声明交换机和两队列, 并将两个队列与该交换机和不同的路由键进行绑定, 路由键可以使用通配符

```java
import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class TopicConfig {

    /**
     * topic交换机
     */
    @Bean
    public TopicExchange topicExchange() {
        return new TopicExchange("my.exchange3", true, false);
    }

    /**
     * topic队列1
     */
    @Bean
    Queue topicQueue1() {
        return new Queue("my.queue5.p1", true);
    }

    /**
     * topic队列2
     */
    @Bean
    Queue topicQueue2() {
        return new Queue("my.queue5.p2", true);
    }

    /**
     * topic队列1绑定到topic交换机和指定的routingKey
     */
    @Bean
    public Binding topicBinding1() {
        return BindingBuilder.bind(topicQueue1()).to(topicExchange()).with("key1.#");
    }

    /**
     * topic队列2绑定到topic交换机和指定的routingKey
     */
    @Bean
    public Binding topicBinding2() {
        return BindingBuilder.bind(topicQueue2()).to(topicExchange()).with("key2.*");
    }
}
```

2. 生产者将消息发送给指定的交换机和路由键

```java
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class TopicProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String msg) {
        // 消息发送到交换机, 并指定routingKey
        rabbitTemplate.convertAndSend("my.exchange3", "key1.a.b.c", msg);
    }
}
```

3. 创建两个消费者, 分表对两个队列进行监听

```java
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class TopicConsumer {

    @RabbitListener(queues = "my.queue5.p1")
    public void listen1(String msg) {
        System.out.println("消费者1监听key1.#:" + msg);
    }

    @RabbitListener(queues = "my.queue5.p2")
    public void listen2(String msg) {
        System.out.println("消费者2监听key2.*:" + msg);
    }
}
```

4. 发送消息

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TopicController {

    @Autowired
    private TopicProducer topicProducer;

    @RequestMapping("/test/topic")
    public String send() {
        topicProducer.send("hello");
        return "发送成功";
    }
}
```
