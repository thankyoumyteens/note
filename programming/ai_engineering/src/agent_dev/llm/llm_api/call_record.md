# LLM 调用记录

调用记录位于 Router 层，用于还原一次请求经历了哪些 Provider、重试和降级；ProviderClient 只提供本次尝试的结果。

## 两类记录

一次业务请求对应一条 `LlmCallRecord`，每尝试一个 Provider 追加一条 `ProviderAttemptRecord`。

| 记录 | 字段 |
| --- | --- |
| `LlmCallRecord` | requestId、traceId、startedAt、endedAt、status、provider、model、usage、totalLatencyMs、fallbackPath、finalError |
| `ProviderAttemptRecord` | provider、model、startedAt、endedAt、status、retryCount、providerLatencyMs、errorType、statusCode |

`fallbackPath` 按实际尝试顺序记录 Provider。`retryCount` 只表示首次请求之后的重试次数。

## 状态

| 状态 | 含义 |
| --- | --- |
| `SUCCESS` | 某个 Provider 返回有效响应 |
| `FAILED` | 调用终止且没有有效响应 |

成功时记录实际命中的 Provider、实际模型和 Token usage；失败时记录最终错误类型和状态码。Provider 未返回 usage 时保留 `null`。

## 时间与耗时

`startedAt` 和 `endedAt` 使用 UTC 时间，用于定位调用；耗时继续复用已有字段：

- `providerLatencyMs`：单个 ProviderClient 的完整耗时，包含内部重试和退避。
- `totalLatencyMs`：整个 Router 调用耗时，包含失败尝试、重试、退避和降级。

耗时使用单调时钟计算，不能用 `endedAt - startedAt` 代替。

## 内容与脱敏

默认不记录 system、messages、模型响应正文和 Provider 原始响应，只记录长度、Token 数和必要元数据。

需要排查内容时，最多保留前 2000 个字符，并在写入前清除 API Key、Authorization、Cookie、密码和其他密钥。异常只记录安全错误说明，不保存请求头和完整响应体。

## 三种实现

| 实现 | Router 总记录 | Provider 尝试记录 |
| --- | --- | --- |
| Spring Boot + WebClient | 在 Router 的 Reactor 调用链结束时写入 | 在每个 ProviderClient 调用的成功或异常信号中追加 |
| Spring AI | 在 Router 返回或抛出异常前写入 | 在同步 ProviderClient 调用的 `try/catch` 中追加 |
| Python + uv | 在 Router 的 `async` 调用结束时写入 | 在每次 `await client.chat()` 的成功或异常分支中追加 |

记录写入失败不能改变 LLM 调用结果；记录器接口应允许替换为日志、数据库或链路追踪实现。

## 过程还原

正常调用的记录包含一条成功的 Provider 尝试；发生降级时，记录按顺序包含失败尝试和最终成功尝试，并通过 `retryCount`、`fallbackPath`、错误信息及两类耗时还原实际过程。
