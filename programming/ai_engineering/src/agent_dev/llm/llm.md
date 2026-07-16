# 最小 LLM 应用

这一阶段把 LLM 作为外部服务接入应用，形成可配置、可切换、可排查的统一调用入口。开始前只需要具备 Java 或 Python 的 HTTP、配置和异常处理基础。

先理解 [LLM 的能力边界](./llm_info/llm_info.md)和[模型与 Provider 的差异](./llm_compare/llm_compare.md)，再进入[大模型 API 调用](./llm_api/llm_api.md)。

API 调用分为两步：

1. 单 Provider Demo：理解三类 API 的请求、响应和错误差异。
2. 统一 Provider 实现：加入统一 DTO、ProviderClient、超时、重试、降级、延迟和调用记录。

实现时选择一条路线：

- [WebClient](./llm_api/spring_boot/spring_boot.md)：直接控制 HTTP 契约。
- [Spring AI](./llm_api/spring_ai/spring_ai.md)：使用 Java 统一模型抽象。
- [Python + uv](./llm_api/python/python.md)：使用官方 SDK，工程调用采用异步实现。
