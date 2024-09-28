# logback 配置

spring boot 默认的日志框架就是 logback。

## 修改日志级别

```yaml
logging:
  level:
    root: debug
```

## 输出到控制台

默认的日志配置就是将日志信息显示到控制台，默认情况下，将会显示 INFO 级别以上的日志信息。

## 输出到文件

```yaml
logging:
  file:
    name: /home/demo/demo.log
```

## 自定义配置文件

```yaml
logging:
  config: classpath:my-config.xml
```
