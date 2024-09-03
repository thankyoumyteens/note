# 开启 GZIP

```yaml
feign:
  # 开启压缩
  compression:
    request:
      enabled: true
      mime-types: text/xml,application/xml,application/json
      # 开启压缩的阈值，单位字节
      min-request-size: 1
    response:
      enabled: true
```
