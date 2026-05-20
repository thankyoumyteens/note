# 第 2 课：接入真实模型 API

本课目标是把第 1 课的 `MockLlmClient` 替换为真实模型调用实现。

一句话概括：

> 本课用 `WebClient` 手写一个 OpenAI-compatible Client，让 `/api/ai/chat` 返回真实大模型回答。

最终调用链从：

```text
AiChatController
  -> AiChatService
  -> LlmClient
  -> MockLlmClient
```

升级为：

```text
AiChatController
  -> AiChatService
  -> LlmClient
  -> OpenAiCompatibleLlmClient
  -> LLM Provider
```

OpenAI 当前推荐新项目使用 Responses API，但 Chat Completions 仍被支持；我们本课继续用 OpenAI-compatible Chat Completions 风格，是因为很多模型供应商和兼容平台都支持这种格式，适合学习底层模型调用机制。
