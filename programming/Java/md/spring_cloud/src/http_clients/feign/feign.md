# Feign

Feign 使服务之间调用更加简单, 只需要声明接口而不用编写实现类。Feign 是基于 Ribbon 实现的，所以它自带了客户端负载均衡功能，也可以通过 Ribbon 的 IRule 进行策略扩展。

Feign 已经停止更新, 最新版本是 1.4.7.RELEASE。

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

    <artifactId>feign-demo</artifactId>
    <packaging>jar</packaging>

    <name>feign-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-feign</artifactId>
            <version>1.4.7.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27436

spring:
  application:
    name: feign-demo

eureka:
  client:
    # 服务注册中心的地址
    serviceUrl:
      defaultZone: http://localhost:27431/eureka/
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
public class FeignDemo {
    public static void main(String[] args) {
        SpringApplication.run(FeignDemo.class, args);
    }
}
```

4. 添加 Feign 接口

```java
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

// 指定服务名
@FeignClient(name = "eureka-client-demo")
public interface DemoFeignClient {

    // 服务中的接口
    @RequestMapping("/service/list")
    List<String> getServiceList();
}
```

5. 通过 Feign 调用服务提供方

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
@RequestMapping("/feign")
public class FController {

    @Autowired
    private DemoFeignClient feignClient;

    @RequestMapping("/test")
    public void test() {
        // 通过FeignClient调用
        List<String> serviceList = feignClient.getServiceList();
        for (Object service : serviceList) {
            System.out.println(service);
        }
    }
}
```
