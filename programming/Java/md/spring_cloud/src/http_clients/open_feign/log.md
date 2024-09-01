# 打印日志

open feign 的日志级别:

- NONE：默认, 不打印日志
- BASIC：仅记录请求方法、URL、响应状态码及执行时间
- HEADERS：除了 BASIC 中定义的信息之外，还有请求和响应的头信息
- FULL：除了 HEADERS 中定义的信息之外，还有请求和响应的正文及元数据

打印日志:

```yaml
feign:
  client:
    config:
      default:
        # feign的日志级别
        loggerLevel: basic

logging:
  level:
    # 要输出日志的FeignClient
    # 日志级别需要设置为debug级别
    com.example.DemoFeignClient: debug
```
