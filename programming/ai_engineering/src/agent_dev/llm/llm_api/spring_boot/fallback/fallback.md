# 降级

ProviderClient：

- 处理 HTTP 状态码
- 处理 timeout
- 处理 retry

ProviderFallbackRouter：

- 处理 provider 降级链
- 记录每个 provider 的失败原因
- 全部失败后抛统一异常

Controller / Service：

- 不写 WebClient 细节
- 不写 provider 降级细节
