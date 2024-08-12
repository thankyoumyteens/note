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

    <artifactId>api-gateway-demo</artifactId>
    <packaging>jar</packaging>

    <name>api-gateway-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
            <version>2.2.10.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27440

spring:
  application:
    name: api-gateway-demo

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
import org.springframework.cloud.netflix.zuul.EnableZuulProxy;

@SpringBootApplication
// 开启Zuul网关代理功能
@EnableZuulProxy
public class ApiGatewayDemo {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayDemo.class, args);
    }
}
```

Spring Cloud Zuul 在整合了 Eureka 之后，具备默认的服务路由功能，Zuul 网关会自动发现 Eureka 中注册的服务, 比如 eureka-client-demo，这时候 Zuul 会创建对应的路由规则。

比如 Zuul 创建的转发到 eureka-client-demo 服务的路由规则为：`/eureka-client-demo/**`。比如访问 http://localhost:27440/eureka-client-demo/service/list，该请求将最终被路由到 eureka-client-demo 的 /service/list 接口上。
