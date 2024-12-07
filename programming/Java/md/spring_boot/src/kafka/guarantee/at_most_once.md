# 最多一次

```yaml
spring:
  kafka:
    consumer:
      bootstrap-servers: localhost:9092
      group-id: test-group
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      enable-auto-commit: true # 启用自动提交
```
