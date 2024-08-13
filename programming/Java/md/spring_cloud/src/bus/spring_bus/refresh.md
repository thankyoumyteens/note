# 配置自动刷新

修改 config-client-demo 项目

1. 添加依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

2. application.yml

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: 123456
    virtual-host: /
```
