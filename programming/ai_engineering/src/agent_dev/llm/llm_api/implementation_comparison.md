# 三种实现能力对照

| 能力 | WebClient | Spring AI | Python + uv |
| --- | --- | --- | --- |
| OpenAI-compatible API | 支持 | 支持 | 支持 |
| OpenAI Responses API | 支持 | 当前 Spring AI 1.1.6 不提供对等原生调用，改用 WebClient | 支持 |
| Anthropic Messages API | 支持 | 支持 | 支持 |
| 统一 DTO | 支持 | 支持 | 支持 |
| Token usage | 从原始响应映射 | 从 `ChatResponse` metadata 映射 | 从 SDK 响应映射 |
| 连接超时 | Reactor Netty | 由底层模型客户端控制 | SDK / HTTP 客户端 |
| 响应超时 | Reactor Netty | 由底层模型客户端控制 | SDK / HTTP 客户端 |
| 请求总超时 | Reactor `timeout` | `CompletableFuture.orTimeout` | SDK timeout |
| 重试和降级 | Reactor Retry + Router | 同步重试循环 + Router | Tenacity + 异步 Router |
| 调用记录 | 支持 | 支持 | 支持 |

三种实现使用相同的统一契约、错误分类、最大尝试次数、退避上限和降级规则；差异只在底层调用方式。
