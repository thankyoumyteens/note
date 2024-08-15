# Spring Cloud Loadbalancer

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

    <artifactId>loadbalancer-consumer</artifactId>
    <packaging>jar</packaging>

    <name>loadbalancer-consumer</name>

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
            <!-- nacos的2.2.x系列，默认引入ribbon, 需要手动去掉 -->
            <!-- 2021.0.x开始去掉ribbon, 引入loadbalancer -->
            <exclusions>
                <exclusion>
                    <groupId>com.netflix.ribbon</groupId>
                    <artifactId>ribbon</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-loadbalancer</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. bootstrap.yml

```yaml
server:
  port: 8020

spring:
  application:
    name: loadbalancer-consumer
  cloud:
    # 配置nacos注册中心地址
    nacos:
      discovery:
        server-addr: localhost:8848
    loadbalancer:
      # 旧版需要手动关闭ribbon
      ribbon:
        enabled: false
```

3. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
public class LoadbalancerConsumer {
    public static void main(String[] args) {
        SpringApplication.run(LoadbalancerConsumer.class, args);
    }
}
```

4. 添加 RestTemplate

```java
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class ConsumerConfig {

    @Bean
    // 开启负载均衡
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

5. 通过 Loadbalancer 调用服务提供方

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
@RequestMapping("/consumer")
public class ConsumerController {

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/hello")
    public String hello() {
        String url = "http://loadbalancer-producer/producer/hello";
        String r = restTemplate.getForObject(url, String.class);
        return r;
    }
}
```
