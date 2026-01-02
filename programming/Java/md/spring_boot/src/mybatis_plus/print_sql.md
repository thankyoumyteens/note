# 打印 SQL

下面的设置只会在控制台中打印出 sql

```yaml
mybatis-plus:
  # 打印sql
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

## 支持把 sql 打印到日志文件中

```yaml
logging:
  level:
    root: info
    # 1. 设置 mybatisplus 包的日志级别为 debug
    com:
      baomidou:
        mybatisplus: debug
    # 2. 设置自己的 mapper 所在包的日志级别为 debug
    com:
      example:
        dao: debug
  # 使用自定义 logback 配置
  config: classpath:logback.xml

mybatis-plus:
  # 3. 使用 mybatisplus 的 slf4j 实现
  configuration:
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl
```
