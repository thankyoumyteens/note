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
    <version>2.0.13</version>
</dependency>
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-log4j12</artifactId>
    <version>2.0.13</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-api</artifactId>
    <version>2.23.1</version>
</dependency>
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.23.1</version>
</dependency>
```

2. resources 下创建 log4j.properties 文件

```conf
log4j.rootLogger=INFO,fileLog,consoleLog
log4j.appender.fileLog=org.apache.log4j.FileAppender
log4j.appender.fileLog.Append=true
log4j.appender.fileLog.Encoding=UTF-8
log4j.appender.fileLog.File=./main.log
log4j.appender.fileLog.layout=org.apache.log4j.PatternLayout
log4j.appender.fileLog.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss.SSS} [%p] %l => %m %n
log4j.appender.consoleLog=org.apache.log4j.ConsoleAppender
log4j.appender.consoleLog.layout=org.apache.log4j.PatternLayout
log4j.appender.consoleLog.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss.SSS} [%p] %l => %m %n
```

3. 输出日志

```java
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class App {
    public static void main(String[] args) {
        log.info("Hello World!");
    }
}
```
