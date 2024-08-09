# 获取配置

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

    <artifactId>config-client-demo</artifactId>
    <packaging>jar</packaging>

    <name>config-client-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
```

2. application.yml

```yaml
server:
  port: 27438

spring:
  application:
    name: config-client-demo
```

3. bootstrap.yml

```yaml
# 必须配置在bootstrap中
spring:
  cloud:
    config:
      # 配置中心地址
      uri: http://localhost:27437
      profile: dev
      # git分支
      label: master
```

4. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConfigClientDemo {
    public static void main(String[] args) {
        SpringApplication.run(ConfigClientDemo.class, args);
    }
}
```

5. 获取配置

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/config")
public class ConfigInfoController {
    @Autowired
    private Environment environment;

    @RequestMapping("/test")
    public String test() {
        return environment.getProperty("myKey");
    }
}
```
