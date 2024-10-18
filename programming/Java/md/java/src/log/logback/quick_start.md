# 基本使用

1. 依赖

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.34</version>
</dependency>
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>2.0.16</version>
</dependency>
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-core</artifactId>
    <version>1.5.7</version>
</dependency>
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.5.7</version>
</dependency>
```

2. resources 下创建 logback.xml 文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!--  输出到控制台  -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <!--设置格式-->
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!--  输出到文件  -->
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <!--设置格式-->
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>utf8</charset>
        </encoder>
        <!--文件路径-->
        <file>/Users/walter/Downloads/main.log</file>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

3. 输出日志

```java
package com.example;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class App {
    public static void main(String[] args) {
        log.info("Hello, World!");
    }
}
```
