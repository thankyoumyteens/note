# Appender

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

## ConsoleAppender

```conf
log4j.rootLogger=INFO,appender1
# 输出到控制台
log4j.appender.appender1=org.apache.log4j.ConsoleAppender
```

## FileAppender

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

## DailyRollingFileAppender

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

## RollingFileAppender

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
