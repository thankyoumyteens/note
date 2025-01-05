# 配置中心

Data ID 的命名规则: `${prefix}-${spring.profiles.active}.${file-extension}`。

- `prefix` 默认为 `spring.application.name` 的值, 也可以通过配置项 `spring.cloud.nacos.config.prefix` 来配置
- `spring.profiles.active` 即为当前环境对应的 profile, 当 `spring.profiles.active` 为空时, 对应的连接符 - 也将不存在, dataId 的拼接格式变成 `${prefix}.${file-extension}`
- `file-exetension` 为配置内容的数据格式, 可以通过配置项 `spring.cloud.nacos.config.file-extension` 来配置。目前只支持 `properties` 和 `yaml` 类型

## 客户端

1. 在 nacos 中创建配置, Data Id 命名为: `nacos-producer-demo.yml`

2. 创建子项目

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

    <artifactId>nacos-config-client</artifactId>
    <packaging>jar</packaging>

    <name>nacos-config-client</name>

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
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
            <version>2.2.9.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

3. 注意是: bootstrap.yml

```yaml
server:
  port: 27442

spring:
  application:
    name: nacos-config-client
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
      config:
        server-addr: localhost:8848
        file-extension: yml
```

4. 获取配置

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

@Component
// 实现配置的动态刷新
@RefreshScope
public class DemoConfigValue {

    @Value("${test}")
    private String test;

    public String getTest() {
        return test;
    }
}
```

5. 使用配置

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/config")
public class ConfigController {

    @Autowired
    private DemoConfigValue demoConfigValue;

    @RequestMapping("/test")
    public String test() {
        return demoConfigValue.getTest();
    }
}
```

6. 访问: http://localhost:27442/config/test
