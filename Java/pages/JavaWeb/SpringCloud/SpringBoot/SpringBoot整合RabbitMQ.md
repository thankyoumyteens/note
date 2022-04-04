# 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

# application.yml

```yaml
spring:
  rabbitmq:
    host: 192.168.1.103
    port: 5672
    username: test
    password: 123456
    virtualHost: /
    # 消息开启手动确认
    listener:
      direct:
        acknowledge-mode: manual
    # 生产者需要配置
    template:
      retry:
        enabled: true
        initial-interval: 10000ms
        max-interval: 300000ms
        multiplier: 2
      # 缺省的交换机名称，此处配置后，发送消息如果不指定交换机就会使用这个
      exchange: topic.exchange
    # 生产者确认机制，确保消息会正确发送，如果发送失败会有错误回执，从而触发重试
    publisher-confirms: true
```

# 配置类

```java
@Configuration
public class RabbitmqConfig {
    public static final String QUEUE_EMAIL = "queue_email";//email队列
    public static final String QUEUE_SMS = "queue_sms";//sms队列
    public static final String EXCHANGE_NAME="topic.exchange";
    public static final String ROUTINGKEY_EMAIL="topic.#.email.#";
    public static final String ROUTINGKEY_SMS="topic.#.sms.#";
 
    //声明交换机
    @Bean(EXCHANGE_NAME)
    public Exchange exchange(){
        //durable(true) 持久化，mq重启之后交换机还在
        return ExchangeBuilder.topicExchange(EXCHANGE_NAME).durable(true).build();
    }
 
    //声明email队列
    /*
     *   new Queue(QUEUE_EMAIL,true,false,false)
     *   durable="true" 持久化 rabbitmq重启的时候不需要创建新的队列
     *   auto-delete 表示消息队列没有在使用时将被自动删除 默认是false
     *   exclusive  表示该消息队列是否只在当前connection生效,默认是false
     */
    @Bean(QUEUE_EMAIL)
    public Queue emailQueue(){
        return new Queue(QUEUE_EMAIL);
    }
    //声明sms队列
    @Bean(QUEUE_SMS)
    public Queue smsQueue(){
        return new Queue(QUEUE_SMS);
    }
 
    //ROUTINGKEY_EMAIL队列绑定交换机，指定routingKey
    @Bean
    public Binding bindingEmail(@Qualifier(QUEUE_EMAIL) Queue queue, @Qualifier(EXCHANGE_NAME) Exchange exchange){
        return BindingBuilder.bind(queue).to(exchange).with(ROUTINGKEY_EMAIL).noargs();
    }
    //ROUTINGKEY_SMS队列绑定交换机，指定routingKey
    @Bean
    public Binding bindingSMS(@Qualifier(QUEUE_SMS) Queue queue, @Qualifier(EXCHANGE_NAME) Exchange exchange){
        return BindingBuilder.bind(queue).to(exchange).with(ROUTINGKEY_SMS).noargs();
    }
}
```

# 生产者

```java
@SpringBootTest
public class Send {
    @Autowired
    RabbitTemplate rabbitTemplate;
    
    @Test
    public void sendMsgByTopics(){
        /**
         * 参数：
         * 1、交换机名称
         * 2、routingKey
         * 3、消息内容
         */
        for (int i=0;i<5;i++){
            String message = "恭喜您，注册成功！userid="+i;
            rabbitTemplate.convertAndSend(RabbitmqConfig.EXCHANGE_NAME,"topic.sms.email",message);
            System.out.println(" [x] Sent '" + message + "'");
        }
    }
}
```

# 消费者

```java
@Component
public class ReceiveHandler {
    //监听邮件队列
    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "queue_email", durable = "true"),
        exchange = @Exchange(
            value = "topic.exchange",
            ignoreDeclarationExceptions = "true",
            type = ExchangeTypes.TOPIC
        ),
        key = {"topic.#.email.#","email.*"}))
    public void rece_email(String msg){
        System.out.println(" [邮件服务] received : " + msg + "!");
    }
 
    //监听短信队列
    @RabbitListener(bindings = @QueueBinding(
        value = @Queue(value = "queue_sms", durable = "true"),
        exchange = @Exchange(
            value = "topic.exchange",
            ignoreDeclarationExceptions = "true",
            type = ExchangeTypes.TOPIC
        ),
        key = {"topic.#.sms.#"}))
    public void rece_sms(String msg){
        System.out.println(" [短信服务] received : " + msg + "!");
    }
}
```
