# 配置文件

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
