# SpringBoot 集成

1. 依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.3.0</version>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
    <version>3.3.0</version>
    <exclusions>
      <exclusion>
        <artifactId>slf4j-api</artifactId>
        <groupId>org.slf4j</groupId>
      </exclusion>
    </exclusions>
  </dependency>
</dependencies>
```

2. application.yml

```yaml
server:
  port: 27431

spring:
  rabbitmq:
    host: 127.0.0.1
    port: 5672
    username: guest
    password: guest
    virtual-host: /
    publisher-returns: true
```

3. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class);
    }
}
```
