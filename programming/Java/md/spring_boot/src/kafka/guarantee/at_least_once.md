# 至少一次

```yaml
spring:
  kafka:
    consumer:
      bootstrap-servers: localhost:9092
      group-id: test-group
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      enable-auto-commit: false # 禁用自动提交
    listener:
      ack-mode: manual_immediate # 手动立即确认
```
