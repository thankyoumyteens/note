# 服务消费方

1. 创建子项目

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
        http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>spring-cloud-demo</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>nacos-client-demo</artifactId>
    <packaging>jar</packaging>

    <name>nacos-client-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
            <version>2.2.9.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27441

spring:
  application:
    name: nacos-client-demo
  cloud:
    nacos:
      # 注册中心地址
      discovery:
        server-addr: localhost:8848
```

3. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
// 开启Feign功能
@EnableFeignClients
public class NacosClientDemo {
    public static void main(String[] args) {
        SpringApplication.run(NacosClientDemo.class, args);
    }
}
```

4. FeignClient

```java
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;

// 指定服务名
@FeignClient(name = "nacos-producer-demo")
public interface DemoFeignClient {

    @RequestMapping("/producer/hello")
    String hello();
}
```

5. 调用外部接口

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/consumer")
public class ConsumerController {

    @Autowired
    private DemoFeignClient demoFeignClient;

    @RequestMapping("/hello")
    public String hello() {
        return demoFeignClient.hello();
    }
}
```

6. 项目启动后, 访问 http://localhost:27441/consumer/hello
