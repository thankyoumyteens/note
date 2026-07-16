# 统一调用契约

三种实现共用同一套业务语义，字段命名按语言习惯使用 camelCase 或 snake_case。

## 请求

| 字段 | 约定 |
| --- | --- |
| system | 可为空，表示没有系统指令 |
| messages | 至少一条，只包含 user 和 assistant |
| options | 为空时使用 temperature=0.2、maxTokens=1000、topP=null |
| metadata | 只传递 requestId、traceId 等扩展信息，不参与核心业务判断 |

Provider 固定为 `openai`、`deepseek`、`anthropic`。

## 响应

| 字段 | 约定 |
| --- | --- |
| provider | 实际成功的 Provider |
| model | Provider 返回的实际模型；未返回时使用请求配置的模型，不能为空 |
| content | 没有文本时返回空字符串 |
| stopReason | 统一为 stop、length、tool_calls、content_filter、other；Provider 未返回时为空 |
| usage | 始终存在；Provider 未返回的 Token 字段使用 null，不能用 0 代替 |
| providerLatencyMs | 最终成功 ProviderClient 的完整耗时，单位毫秒 |
| totalLatencyMs | 整个 Router 调用耗时，单位毫秒 |
| metadata | 保存响应 ID、原始停止原因等扩展信息，不承载核心业务字段 |

## 错误

单个 Provider 失败统一使用 `LlmProviderException`，包含 Provider、状态码、安全的错误说明和可选响应体；无 HTTP 状态的超时或网络错误使用 `-1`。

所有 Provider 都失败统一使用 `AllProvidersFailedException`，按实际调用顺序保存每个 Provider 的失败原因。
