# 切换数据传输方式

zipkin 默认的传输方式是 HTTP, 一旦传输过程中客户端和服务端断掉了, 那么这条跟踪日志信息将会丢失。生产中推荐使用 MQ 传输。

## 服务端添加 RabbitMQ

```sh
java -jar zipkin-server-2.27.1-exec.jar --zipkin.collector.rabbitmq.addresses=localhost:5672 --zipkin.collector.rabbitmq.username=guest --zipkin.collector.rabbitmq.password=guest
```

## 客户端添加 RabbitMQ

1. 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

2. 所有服务的配置文件

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    virtual-host: /
  cloud:
    sleuth:
      sampler:
        probability: 1.0
    zipkin:
      sender:
        type: rabbit
      discovery-client-enabled: false
```

3. 启动项目, 并调用微服务的任意接口
4. 打开 http://localhost:9411, 进入"找到一个痕迹"页签, 点击 RUN QUERY 按钮可以看到刚才调用的接口, 点击 SHOW 进入详情查看服务调用的相关信息。进入"依赖"页签, 点击 RUN QUERY 按钮, 可以查看每个服务的依赖
