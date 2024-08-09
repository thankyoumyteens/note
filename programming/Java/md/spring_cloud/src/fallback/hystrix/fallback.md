# 服务降级

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

    <artifactId>hystrix-demo</artifactId>
    <packaging>jar</packaging>

    <name>hystrix-demo</name>

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
            <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>
            <version>2.2.10.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
            <version>2.2.10.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27439

spring:
  application:
    name: hystrix-demo

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
import org.springframework.cloud.netflix.hystrix.EnableHystrix;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
// 开启断路器功能, 也可以用@EnableCircuitBreaker
@EnableHystrix
public class HystrixDemo {
    public static void main(String[] args) {
        SpringApplication.run(HystrixDemo.class, args);
    }
}
```

4. 设置负载均衡

```java
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class HConfig {

    @Bean
    // 开启Ribbon负载均衡
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

5. 在调用服务的方法上使用 `@HystrixCommand` 注解来指定服务降级方法

```java
import com.netflix.hystrix.contrib.javanica.annotation.HystrixCommand;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
@RequestMapping("/hystrix")
public class HController {

    @Autowired
    private RestTemplate restTemplate;

    /**
     * 服务降级方法
     */
    public String fallback() {
        return "请稍后重试";
    }

    @RequestMapping("/test")
    // 指定服务降级方法
    @HystrixCommand(fallbackMethod = "fallback")
    public String test() {
        // 直接通过服务名调用
        String url = "http://eureka-client-demo/service/list";
        List serviceList = restTemplate.getForObject(url, List.class);
        for (Object service : serviceList) {
            System.out.println(service);
        }
        return "ok";
    }
}
```

6. 在服务提供方加上 `Thread.sleep(10000);` 来模拟请求超时, 触发降级
