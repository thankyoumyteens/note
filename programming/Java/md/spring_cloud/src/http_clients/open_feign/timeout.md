# 设置超时时间

```yaml
feign:
  client:
    config:
      # 设置全局超时时间
      default:
        # 建立连接后从服务器读取可用资源所用的时间
        connectTimeout: 5000
        # 建立连接所用的时间
        readTimeout: 5000
      # 为service1服务单独配置超时时间
      service1:
        connectTimeout: 3000
        readTimeout: 3000
```
