# log4j

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
log4j.rootLogger=INFO,CONSOLE
log4j.appender.CONSOLE=org.apache.log4j.ConsoleAppender
log4j.appender.CONSOLE.layout=org.apache.log4j.PatternLayout
log4j.appender.CONSOLE.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss} %-5p %c{1}:%L - %m%n
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

## 配置

Log4j 支持两种配置文件格式:

- XML 文件
- properties 文件

```conf
log4j.rootLogger = level, appenderName1, appenderName2, ...
# 表示Logger不会在父Logger的appender里输出, 默认为true
log4j.additivity.org.apache=true
```

- level: 设定日志记录的最低级别, 可设的值有 OFF, FATAL, ERROR, WARN, INFO, DEBUG, ALL 或者自定义的级别
- appenderNameX: 设置 Appender, Appender 用来控制日志输出的位置

## Appender

Appender 用来控制日志输出的位置。

```conf
log4j.appender.appenderName = className
```

- appenderName: Appender 的名称, 自定义。在 log4j.rootLogger 中使用
- className: 指定 Appender 类, 可选的值:
  - org.apache.log4j.ConsoleAppender: 输出到控制台
  - org.apache.log4j.FileAppender: 输出到文件
  - org.apache.log4j.DailyRollingFileAppender: 每天产生一个日志文件
  - org.apache.log4j.RollingFileAppender: 文件大小到达指定尺寸的时候产生一个新的文件
  - org.apache.log4j.WriterAppender: 将日志信息以流格式发送到任意指定的地方

每个 Appender 都可以设置自己的参数。

### ConsoleAppender

```conf
log4j.rootLogger=INFO,appender1
# 输出到控制台
log4j.appender.appender1=org.apache.log4j.ConsoleAppender
```

### FileAppender

```conf
log4j.rootLogger=INFO,appender1
# 输出到文件
log4j.appender.appender1=org.apache.log4j.FileAppender
# true: 日志追加到文件中
# false: 覆盖文件
log4j.appender.appender1.Append=false
# 日志文件编码
log4j.appender.appender1.Encoding=UTF-8
# 日志文件路径
log4j.appender.appender1.File=/my_projct/logs/main.log
```

### DailyRollingFileAppender

```conf
log4j.rootLogger=INFO,appender1
# 输出到文件
log4j.appender.appender1=org.apache.log4j.DailyRollingFileAppender
# true: 日志追加到文件中
# false: 覆盖文件
log4j.appender.appender1.Append=false
# 日志文件编码
log4j.appender.appender1.Encoding=UTF-8
# 日志文件路径
log4j.appender.appender1.File=/my_projct/logs/main.log
# 日志文件生成规则
# 每分钟生成一个文件
# 前一分钟的日志文件名为main.log.2020-01-01-10-11
log4j.appender.appender1.DatePattern='.'yyyy-MM-dd-HH-mm
```

### RollingFileAppender

```conf
log4j.rootLogger=INFO,appender1
# 输出到文件
log4j.appender.appender1=org.apache.log4j.RollingFileAppender
# true: 日志追加到文件中
# false: 覆盖文件
log4j.appender.appender1.Append=false
# 日志文件编码
log4j.appender.appender1.Encoding=UTF-8
# 日志文件路径
log4j.appender.appender1.File=/my_projct/logs/main.log
# 在日志文件达到10MB时, 将原来的内容移到main.log.1文件中
log4j.appender.appender1.MaxFileSize=10MB
# 可以产生的滚动文件的最大数量
# 设为2则可以产生main.log.1, main.log.2两个滚动文件和一个main.log文件
log4j.appender.appender1.MaxBackupIndex=2
```

## Layouts

Log4j 可以在 Appenders 的后面附加 Layouts 来指定日志输出的样式。

```conf
log4j.appender.appenderName.layout = className
```

- appenderName: Appender 的名称, 自定义。在 log4j.rootLogger 中使用
- className: 指定 Layouts 类, 可选的值:
  - org.apache.log4j.HTMLLayout: 以 HTML 表格形式布局
  - org.apache.log4j.PatternLayout: 自定义布局模式
  - org.apache.log4j.SimpleLayout: 包含日志信息的级别和信息字符串
  - org.apache.log4j.TTCCLayout: 包含日志产生的时间、线程、类别等信息

### PatternLayout

```conf
log4j.rootLogger=INFO,appender1
# 输出到控制台
log4j.appender.appender1=org.apache.log4j.ConsoleAppender
# 为appender1指定Layouts
log4j.appender.appender1.layout=org.apache.log4j.PatternLayout
# 为appender1的PatternLayout设置输出格式
log4j.appender.appender1.layout.ConversionPattern=[%p] %m %n
```

## ConversionPattern 配置

- `%p`: 输出日志的级别, 即 DEBUG, INFO, WARN, ERROR, FATAL
- `%d`: 输出日志发生时间, 可以在其后指定格式, 如: `%d{yyyy/MM/dd HH:mm:ss,SSS}`
- `%r`: 输出自应用程序启动到输出该 log 信息耗费的毫秒数
- `%t`: 输出产生该日志事件的线程名
- `%l`: 输出日志事件的发生位置, 相当于 `%c.%M(%F:%L)` 的组合, 包括类全名、方法、文件名以及在代码中的行数
- `%c`: 输出日志信息所属的类全名
- `%M`: 输出产生日志信息的方法名
- `%F`: 输出日志消息产生时所在的文件名称
- `%L`: 输出代码中的行号
- `%m`: 输出代码中指定的具体日志信息
- `%n`: 输出一个换行符
- `%x`: 输出和当前线程相关联的 NDC(嵌套诊断环境)
- `%%`: 输出一个 `%` 字符

另外, 还可以在 `%` 与格式字符之间加上修饰符来控制其最小长度, 最大长度, 和文本的对齐方式。如:

1. `%100c`: 类全名的最小长度为 100 个字符, 不足的用空格补全, 内容右对齐
2. `%-100c`: 类全名的最小长度为 100 个字符, 不足的用空格补全, 内容左对齐
3. `%.100c`: 类全名的最大长度为 100 个字符, 超出部分从左边截断, 不足也不会补空格
