# Python

这条路线使用 `uv` 管理项目和依赖，直接调用 OpenAI、Anthropic 官方 SDK。

三类基础 API Demo 使用同步客户端，便于观察原始请求和响应；完整 fallback 示例使用异步客户端、FastAPI 和异步 Router，避免网络等待阻塞事件循环。先完成单 Provider Demo，再进入异步的统一 DTO、ProviderClient、重试和降级。
