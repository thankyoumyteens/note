# Spring AI

Spring AI 通过 `ChatClient` 和 `ChatModel` 统一不同 Provider 的常见模型调用，减少业务代码对底层 HTTP 协议和 SDK 的依赖。

统一抽象不保证覆盖 Provider 的全部原生 API。当前项目使用 Spring AI 1.1.6，OpenAI Responses API 需要改用 WebClient，详见[调用 OpenAI Responses API](./responses_api.md)。

基础 Demo 先了解 `ChatClient` 如何调用 OpenAI-compatible 和 Anthropic；需要多 Provider 切换时，再进入 fallback，将 Spring AI 响应、异常、重试和降级映射到统一契约。
