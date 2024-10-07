# 统一 JVM 日志记录

使用 JVM 参数 `-Xlog` 打印日志。

格式:

```sh
-Xlog[:[what][:[output][:[decorators][:output-options[,...]]]]]
```

- what: 指定日志的 tag 和 level
- output: 日志输出到哪里
- decorators: 日志格式
- output-options: 日志的其它设置
