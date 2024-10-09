# JVM 统一日志框架

JVM 统一日志框架为 JVM 的所有组件提供了一个通用的日志记录系统。垃圾回收的日志也改用这个新框架了。

使用 JVM 参数 `-Xlog` 打印日志。格式:

```sh
-Xlog[:[what][:[output][:[decorators][:output-options[,...]]]]]
```

- what: 指定日志的 tag 和 level
- output: 日志输出到哪里
- decorators: 日志格式
- output-options: 日志的其它设置

## Tag 和 Level
