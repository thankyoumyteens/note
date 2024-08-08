# 创建注册中心

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

    <artifactId>eureka-server-demo</artifactId>
    <packaging>jar</packaging>

    <name>eureka-server-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27431

spring:
  application:
    name: eureka-server-demo

eureka:
  instance:
    hostname: localhost
  client:
    # 默认也会将自己作为客户端来尝试注册，手动关闭
    # 是否将自己注册到Eureka Server中
    registerWithEureka: false
    # 是否从Eureka Server中获取注册的服务信息
    fetchRegistry: false
```

3. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
// 开启Eureka服务端功能
@EnableEurekaServer
public class EurekaServerDemo {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerDemo.class, args);
    }
}
```

4. 项目启动后, 访问 http://localhost:27431/ 打开管理页面
