# 搭建

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

    <artifactId>gateway-demo</artifactId>
    <packaging>jar</packaging>

    <name>gateway-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
            <version>2.2.9.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-gateway</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 8090

spring:
  application:
    name: gateway-demo
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
    gateway:
      routes:
        - id: myRoute1
          # 格式 lb://服务名
          # 通过全局过滤器LoadBalancerClientFilter负责路由寻址和负载均衡
          uri: lb://nacos-client-demo
          predicates:
            - Path=/test/**
```

3. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
public class GatewayDemo {
    public static void main(String[] args) {
        SpringApplication.run(GatewayDemo.class, args);
    }
}
```

4. 启动网关和一个服务提供方, 访问 http://localhost:8090/test/hello, 请求会被路由到 http://nacos-client-demo/test/hello

注意: 新版本 spring-cloud-starter-gateway 移除了负载均衡依赖, 所以需要手动添加 spring-cloud-loadbalancer。
