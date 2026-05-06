# 第 2 课：接入真实模型 API

本课目标是把第 1 课中的 `MockLlmClient` 替换为真实模型调用。

调用链从：

```text
Controller -> Service -> MockLlmClient
```

升级为：

```text
Controller
  -> Service
  -> LlmClient
  -> OpenAiCompatibleLlmClient
  -> LLM Provider
```

最终实现：

```http
POST /api/ai/chat
```

调用真实大模型并返回真实回答。

## 为什么要先手写模型 Client？

后续可以使用 Spring AI，但第 2 课选择先手写 `OpenAiCompatibleLlmClient`。

原因：

- 理解模型 API 的底层 HTTP 结构
- 理解 `messages`、`model`、`temperature` 等核心参数
- 理解 WebClient 如何调用外部 API
- 理解 API Key、超时、错误处理
- 为后续流式输出、结构化输出、Function Calling 打基础

如果一开始就使用高级框架，容易只会“调框架”，但不理解模型调用本质。
