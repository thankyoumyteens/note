# Python 错误处理

Python 路线在异步 ProviderClient 中把 SDK 异常转换为 `LlmProviderException`，Router 只处理统一异常。

## 异常映射

| SDK 异常 | 统一状态码 |
| --- | --- |
| OpenAI / Anthropic 超时 | `-1` |
| OpenAI / Anthropic 连接、DNS、断网错误 | `-1` |
| SDK HTTP 状态异常 | Provider 返回的 HTTP 状态码 |

`-1` 表示调用没有收到 HTTP 响应，不能伪造为 408、500 或 503。

## 处理规则

| 状态 | 重试 | 降级 |
| --- | --- | --- |
| 400、401、403 | 否 | 否 |
| 429 | 当前 Provider 重试耗尽后 | 是 |
| 500、502、503、504 | 当前 Provider 重试耗尽后 | 是 |
| `-1` | 当前 Provider 重试耗尽后 | 是 |

ProviderClient 负责 SDK 异常转换和当前 Provider 重试；Router 负责跨 Provider 降级。Router 不捕获普通 `Exception`，避免把代码错误伪装成网络错误。

ProviderClient、Router 和 FastAPI endpoint 全部使用 `async def` / `await`，不混入同步 SDK 或同步网络请求。

对应代码见[自定义异常](./fallback/ex.md)、[ProviderClient](./fallback/provider_clients.md)和[显式 Provider 降级链](./fallback/router.md)。
