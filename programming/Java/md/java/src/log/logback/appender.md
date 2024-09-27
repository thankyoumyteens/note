# Appender

负责输出日志

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    </appender>
</configuration>
```

- name: Appender 名称
- class: Appender 使用的类

## ConsoleAppender

日志输出到控制台

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <!--  日志格式  -->
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>utf8</charset>
        </encoder>
        <!--  输出位置  -->
        <!--  可选值:  -->
        <!--      System.out 默认  -->
        <!--      System.err  -->
        <target>System.out</target>
    </appender>
</configuration>
```

## FileAppender

日志输出到文件

```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <!--  日志格式  -->
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>utf8</charset>
        </encoder>
        <!--  日志文件路径  -->
        <file>./main.log</file>
        <!--  日志是否加到文件末尾  -->
        <append>true</append>
    </appender>
</configuration>
```

## RollingFileAppender

自动创建日志文件

```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!--  日志格式  -->
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
            <charset>utf8</charset>
        </encoder>
        <!--  日志文件生成策略  -->
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!--  每天生成一个日志文件  -->
            <fileNamePattern>./main.%d{yyyy-MM-dd}.log</fileNamePattern>
            <!--  每个日志文件最大的保存时间  -->
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>
</configuration>
```
