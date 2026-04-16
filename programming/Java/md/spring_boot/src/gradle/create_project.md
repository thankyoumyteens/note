# 项目搭建(JDK25)

### 1. 环境依赖要求

- JDK: Java 25 (推荐使用 LTS 版本或最新的 GA 版本)。
- Gradle: 需要 8.14 或 9.x 以上版本，以全面支持 Java 25 的字节码。
- Jakarta EE: 4.0 版本要求 Jakarta EE 11。

### 2. 目录结构搭建

```
spring-boot-demo-25/
├── build.gradle
├── settings.gradle
└── src/
    └── main/
        ├── java/
        │   └── com/example/demo/
        │       └── Application.java
        └── resources/
            └── application.properties
```

手动创建以上目录结构（或者在 IDEA 中新建一个空的 Gradle 项目）：

```sh
mkdir spring-boot-demo-25
cd spring-boot-demo-25
touch build.gradle
touch settings.gradle
mkdir -p src/main/java/com/example/demo/
touch src/main/java/com/example/demo/Application.java
mkdir -p src/main/resources/
touch src/main/resources/application.properties
```

### 3. settings.gradle

指定项目名称：

```groovy
rootProject.name = 'spring-boot-demo-25'
```

### 4. build.gradle

```groovy
plugins {
    id 'java'
    // 使用 2026 年 3 月发布的正式版
    id 'org.springframework.boot' version '4.0.5'
    id 'io.spring.dependency-management' version '1.1.7'
}

group = 'com.example'
version = '1.0.0-SNAPSHOT'

java {
    toolchain {
        // 强制使用 Java 25
        languageVersion = JavaLanguageVersion.of(25)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // 基础核心：Spring Boot 4.0 将核心功能进一步解耦
    // 仅包含 IoC 容器、日志、YAML 配置等
    implementation 'org.springframework.boot:spring-boot-starter'

    // 测试套件：默认包含 JUnit 5 和 AssertJ
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

tasks.named('test') {
    useJUnitPlatform()
}
```

### 5. Application.java

```java
package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
public class Application {

    private static final Logger log = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        // Spring Boot 4.0 启动默认开启了虚拟线程支持（如果运行在 Java 21+）
        SpringApplication.run(Application.class, args);
    }

    @Bean
    public CommandLineRunner runner() {
        return args -> {
            log.info("--- Spring Boot 4.0.5 系统启动 ---");
            log.info("当前 JDK 版本: {}", System.getProperty("java.version"));
            log.info("核心容器已就绪。");

            // 示例：Java 25 预览特性：灵活的构造函数主体或模式匹配增强
            String status = "ACTIVE";
            var message = switch (status) {
                case String s when s.equalsIgnoreCase("active") -> "系统运行中";
                default -> "未知状态";
            };
            log.info("状态检查: {}", message);
        };
    }
}
```

### 6. 生成特定版本的 Wrapper

为了生成 Wrapper，你的电脑上需要先有一个安装好的 Gradle：

```sh
brew install gradle
gradle -v
```

生成 Wrapper：

```sh
gradle wrapper --gradle-version 9.4.1 --distribution-type all
```

执行完成后，你会发现目录中多出了以下文件：

- gradlew (Unix/macOS 脚本)
- gradlew.bat (Windows 脚本)
- gradle/wrapper/gradle-wrapper.jar
- gradle/wrapper/gradle-wrapper.properties

### 7. 下载 Gradle 并运行项目

在网络环境受限时，务必使用以下命令。注意增加了 SOCKS5 备选方案 和 更长的超时时间。

```sh
chmod +x gradlew

# 注入代理并强制延长 Java 25 的握手超时时间
export GRADLE_OPTS="-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=7890 \
  -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=7890 \
  -Dsun.net.client.defaultConnectTimeout=600000 \
  -Dsun.net.client.defaultReadTimeout=600000 \
  -Djava.net.preferIPv4Stack=true"

./gradlew bootRun
```

### 8. 使用 IDEA 打开项目

1. 导入: File -> Open 选择该项目。
2. 配置 SDK: 在 Project Structure -> Project 中选择 JDK 25。
3. 配置 Gradle:
   - Settings -> Build, Execution, Deployment -> Build Tools -> Gradle
   - Gradle JVM: 选 Project SDK (25)。
   - HTTP Proxy: 如果 IDEA 报错，同步设置 IDEA 的 System Settings -> HTTP Proxy。
