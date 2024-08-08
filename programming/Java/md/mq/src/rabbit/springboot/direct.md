# Direct

1. 配置类, 声明交换机和两队列, 并将两个队列与该交换机和不同的路由键进行绑定

```java
import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class DirectConfig {

    /**
     * direct交换机
     */
    @Bean
    public DirectExchange directExchange() {
        return new DirectExchange("my.exchange2", true, false);
    }

    /**
     * direct队列1
     */
    @Bean
    Queue directQueue1() {
        return new Queue("my.queue4.p1", true);
    }

    /**
     * direct队列2
     */
    @Bean
    Queue directQueue2() {
        return new Queue("my.queue4.p2", true);
    }

    /**
     * direct队列1绑定到direct交换机和指定的routingKey
     */
    @Bean
    public Binding directBinding1() {
        return BindingBuilder.bind(directQueue1()).to(directExchange()).with("key1");
    }

    /**
     * direct队列2绑定到direct交换机和指定的routingKey
     */
    @Bean
    public Binding directBinding2() {
        return BindingBuilder.bind(directQueue2()).to(directExchange()).with("key2");
    }
}
```

2. 生产者将消息发送给指定的交换机和路由键

```java
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class DirectProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String msg) {
        // 消息发送到交换机, 并指定routingKey
        rabbitTemplate.convertAndSend("my.exchange2", "key2", msg);
    }
}
```

3. 创建两个消费者, 分表对两个队列进行监听

```java
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class DirectConsumer {

    @RabbitListener(queues = "my.queue4.p1")
    public void listen1(String msg) {
        System.out.println("消费者1监听key1:" + msg);
    }

    @RabbitListener(queues = "my.queue4.p2")
    public void listen2(String msg) {
        System.out.println("消费者2监听key2:" + msg);
    }
}
```

4. 发送消息

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DirectController {

    @Autowired
    private DirectProducer directProducer;

    @RequestMapping("/test/direct")
    public String send() {
        directProducer.send("hello");
        return "发送成功";
    }
}
```
