# Layouts

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

## PatternLayout

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
