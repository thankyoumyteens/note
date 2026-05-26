# 第 9 课：Spring AI 框架适配与生态入口

本课解决的问题：

```text
我们已经手写了 OpenAI-compatible Client。
现在要学习 Spring AI，但不能破坏已有 AI Gateway 架构。
```

一句话概括：

> 本课新增 `SpringAiLlmClient`，让 Spring AI 成为 `LlmClient` 的另一个实现，并通过配置在手写 Client 和 Spring AI Client 之间切换。

本课不做：

```text
不做 Spring AI RAG
不做 Spring AI VectorStore
不做 Spring AI Tool Calling
不做 Spring AI Observability 深入
不让 Controller 直接使用 ChatClient
不让业务 Service 直接依赖 Spring AI
```
