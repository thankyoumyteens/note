# Encoder

encoder 节点的默认值是 PatternLayoutEncoder。

```xml
<encoder>
    <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    <charset>utf8</charset>
</encoder>
```

## pattern 配置

- `%c{length}`: 日志的 logger 名。length 可选, 用来缩短输出字符串的长度, 设置为 0 表示只输出最右边的 `.` 之后的字符串
- `%C{length}`: 日志信息所属的类全名。length 可选, 用来缩短输出字符串的长度, 设置为 0 表示只输出最右边的 `.` 之后的字符串
- `%d{pattern}`: 日志的产生时间。pattern 用来格式化日期, 例如: `%d{yyyy-MM-dd HH:mm:ss.SSS}`
- `%F`: 输出日志信息所属的文件名
- `%caller{depth}`: 日志的调用链路。例如, `%caller{5}` 输出:
  ```log
  Caller+0	 at com.example.App.say(App.java:9)
  Caller+1	 at com.example.App.main(App.java:12)
  ```
- `%L`: 打印日志的代码所在的行号
- `%m`: 应用程序提供的信息
- `%M`: 打印日志的代码所在的方法名
- `%n`: 换行
- `%p`: 日志级别
- `%t`: 产生日志的线程名
