# 第 8 课：重试、限流、Fallback

## 本课要解决什么问题

现在你的 AI Gateway 已经能调用模型，但还缺少稳定性保护。

模型供应商可能出现：

```text
请求超时
临时 500
429 限流
网络抖动
模型服务不可用
响应为空
```

如果没有治理，这些问题会直接影响你的业务接口。

一句话概括本课：

> 本课要给模型调用增加重试、限流和 fallback，防止模型供应商异常影响主服务。

## 当前为什么不用 Resilience4j？

生产系统推荐用 Resilience4j：

```text
Retry
RateLimiter
CircuitBreaker
Bulkhead
TimeLimiter
```

但你现在还在学习 AI Gateway 底层原理，所以本课先手写简单版本。

目的：

```text
先理解机制，再引入框架。
```

后面可以把手写逻辑替换成 Resilience4j。
