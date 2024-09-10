# LoadBalancerClient

LoadBalancerClient 是 SpringCloud 提供的一种负载均衡客户端。

LoadBalancerClient 在初始化时会通过 Eureka Client 向 Eureka 服务端获取所有服务实例的注册信息并缓存在本地, 并且每 10 秒向 EurekaClient 发送 “ping”, 来判断服务的可用性。如果服务的可用性发生了改变或者服务数量和之前的不一致, 则更新或者重新拉取。最后, 在得到服务列表后, ILoadBalancer 会根据 IRule 的策略进行负载均衡(默认策略为轮询)。

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

    <artifactId>lbc-demo</artifactId>
    <packaging>jar</packaging>

    <name>lbc-demo</name>

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
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27434

spring:
  application:
    name: lbc-demo

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
public class LbcDemo {
    public static void main(String[] args) {
        SpringApplication.run(LbcDemo.class, args);
    }
}
```

4. 添加 RestTemplate

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class LdcConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

5. 通过 LoadBalancerClient 获取服务提供方并调用

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.loadbalancer.LoadBalancerClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@RestController
@RequestMapping("/ldc")
public class LdcController {

    @Autowired
    private LoadBalancerClient loadBalancerClient;

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/test")
    public void test() {
        // 根据 service ID 获取服务提供方
        ServiceInstance serviceInstance = loadBalancerClient.choose("eureka-client-demo");
        String url = "http://" + serviceInstance.getHost() + ":" + serviceInstance.getPort() + "/service/list";
        // 调用
        List serviceList = restTemplate.getForObject(url, List.class);
        for (Object service : serviceList) {
            System.out.println(service);
        }
    }
}
```
