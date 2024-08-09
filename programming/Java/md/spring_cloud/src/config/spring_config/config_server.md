# Config Server

1. 创建 git 仓库(以 gitee 为例)

2. 仓库中添加两个文件

```yaml
# config-client-demo.yml
myKey: myVal

# config-client-demo-dev.yml
abc: 123
```

3. 创建子项目

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

    <artifactId>config-server-demo</artifactId>
    <packaging>jar</packaging>

    <name>config-server-demo</name>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>
    </dependencies>
</project>
```

4. application.yml

```yaml
server:
  port: 27437

spring:
  application:
    name: config-server-demo
  cloud:
    config:
      server:
        git:
          uri: https://gitee.com/xxxxxx.git
          username: 用户名
          password: 密码
```

5. 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
// 开启配置中心功能
@EnableConfigServer
public class ConfigServerDemo {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerDemo.class, args);
    }
}
```

6. 项目启动后, 访问 http://localhost:27437/config-client-demo.yml 和 http://localhost:27437/config-client-demo-dev.yml 即可访问两个配置文件
