# Fanout

1. 配置类, 声明交换机和两队列, 并将两个队列与该交换机进行绑定

```java
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.FanoutExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class FanoutConfig {

    /**
     * fanout交换机
     */
    @Bean
    public FanoutExchange fanoutExchange() {
        return new FanoutExchange("my.exchange1", true, false);
    }

    /**
     * fanout队列1
     */
    @Bean
    Queue fanoutQueue1() {
        return new Queue("my.queue3.p1", true);
    }

    /**
     * fanout队列2
     */
    @Bean
    Queue fanoutQueue2() {
        return new Queue("my.queue3.p2", true);
    }

    /**
     * fanout队列1绑定到fanout交换机
     */
    @Bean
    public Binding binding1() {
        return BindingBuilder.bind(fanoutQueue1()).to(fanoutExchange());
    }

    /**
     * fanout队列2绑定到fanout交换机
     */
    @Bean
    public Binding binding2() {
        return BindingBuilder.bind(fanoutQueue2()).to(fanoutExchange());
    }
}
```

2. 生产者将消息发送给交换机

```java
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FanoutProducer {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String msg) {
        // 消息发送到交换机, Fanout模式不需要路由键
        rabbitTemplate.convertAndSend("my.exchange1", "", msg);
    }
}
```

3. 创建两个消费者, 分表对两个队列进行监听

```java
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class FanoutConsumer {

    @RabbitListener(queues = "my.queue3.p1")
    public void listen1(String msg) {
        System.out.println("消费者1:" + msg);
    }

    @RabbitListener(queues = "my.queue3.p2")
    public void listen2(String msg) {
        System.out.println("消费者2:" + msg);
    }
}
```

4. 发送消息

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanoutController {

    @Autowired
    private FanoutProducer fanoutProducer;

    @RequestMapping("/test/fanout")
    public String send() {
        fanoutProducer.send("hello");
        return "发送成功";
    }
}
```
