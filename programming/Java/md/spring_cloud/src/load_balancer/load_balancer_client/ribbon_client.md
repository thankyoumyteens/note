# Ribbon

Ribbon 使用起来更加方便, 它的 url 格式: `http://服务名/接口`, 它能够在进行调用的时候, 自动选取服务实例, 并将服务名替换成实际要请求的 IP 地址和端口, 从而完成服务接口的调用。省略了 LoadBalancerClient 选取服务实例和拼接 URL 的步骤, 直接通过 RestTemplate 发起请求。

Ribbon 已经停止更新, 最新版本是 2.2.10.RELEASE。

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

    <artifactId>ribbon-demo</artifactId>
    <packaging>jar</packaging>

    <name>ribbon-demo</name>

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
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27435

spring:
  application:
    name: ribbon-demo

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

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
public class RibbonDemo {
    public static void main(String[] args) {
        SpringApplication.run(RibbonDemo.class, args);
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
public class RConfig {

    @Bean
    // 开启Ribbon负载均衡
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

5. 通过 Ribbon 调用服务提供方

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.loadbalancer.LoadBalancerClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
@RequestMapping("/ribbon")
public class RController {

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/test")
    public void test() {
        // 直接通过服务名调用
        String url = "http://eureka-client-demo/service/list";
        List serviceList = restTemplate.getForObject(url, List.class);
        for (Object service : serviceList) {
            System.out.println(service);
        }
    }
}
```
