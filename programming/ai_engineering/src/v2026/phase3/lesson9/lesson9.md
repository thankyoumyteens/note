# 第 9 课：Spring AI 重构

## 本课要解决什么问题

前面 8 课你手写了一个完整的 OpenAI-compatible Client，包括：

```text
WebClient 调模型
流式输出
结构化输出
工具调用
调用日志
限流
重试
fallback
```

这很好，因为你已经理解了底层原理。

但继续往后做 RAG、Embedding、Vector Store、Tool Calling、Observability，如果全部手写，复杂度会越来越高。

Spring AI 的定位是把 Spring 生态里的可移植、模块化、POJO 设计原则带到 AI 应用开发中，并用于连接企业数据、API 和 AI 模型。官方文档也说明，Spring AI 提供 Spring-friendly API 和抽象，用于构建 AI 应用。

一句话概括本课：

> 本课要在保留 `LlmClient` 抽象的前提下，引入 Spring AI，并用 Spring AI `ChatClient` 实现一个新的基础聊天 Client。

## 当前版本兼容性注意

项目目前是：

```text
Spring Boot 3.2.4
Java 21
```

但 Spring AI 当前官方 Getting Started 文档写明：Spring AI 支持 Spring Boot 3.4.x 和 3.5.x。

Spring AI GitHub README 也显示了不同 Spring AI 分支与 Spring Boot 的兼容关系，例如 Spring AI 1.1.x 对应 Spring Boot 3.5.x，Spring AI 2.x 对应 Spring Boot 4.x。

所以本课会把项目从：

```text
Spring Boot 3.2.4
```

升级到：

```text
Spring Boot 3.4.x / 3.5.x
```

然后引入 Spring AI。
