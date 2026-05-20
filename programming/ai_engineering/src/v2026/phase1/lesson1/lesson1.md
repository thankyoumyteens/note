# 第 1 课：先建立 AI Gateway 的工程模型

本课目标是建立 AI Gateway 的最小 Spring Boot 项目骨架，先跑通：

```text
Controller -> Service -> LlmClient -> MockLlmClient
```

一句话概括：

> 本课不接真实模型，只用 Mock 实现跑通第一个 AI Gateway 接口，并建立后续所有模型调用的分层基础。

最终实现接口：

```http
POST /api/ai/chat
```

## 什么是 AI Gateway？

AI Gateway 是业务系统和大模型之间的统一接入层。

它不是简单地把请求转发给模型，而是负责把模型能力包装成稳定的后端能力。

典型职责包括：

- 统一模型调用入口
- 屏蔽不同模型供应商差异
- 管理 API Key
- 管理超时和错误
- 支持流式输出
- 支持结构化输出
- 支持 Function Calling
- 支持调用日志
- 支持成本统计
- 支持重试、限流、fallback
- 为后续 RAG、Agent、MCP 提供基础

当前阶段的最小 AI Gateway 是：

```text
用户请求
  -> Spring Controller
  -> Service
  -> LlmClient
  -> Mock 或真实模型实现
```

### 1. 普通后端接口长这样

传统 Java 后端一般是：

```text
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```

例如：

```text
GET /api/orders/123
  ↓
查数据库
  ↓
返回订单 JSON
```

这是确定性的。

---

### 2. AI Gateway 长这样

AI 应用后端更像：

```text
Controller
  ↓
AI Service
  ↓
Prompt Builder
  ↓
Model Client
  ↓
LLM Provider
  ↓
Response Validator
  ↓
返回结果
```

例如：

```text
POST /api/ai/chat
  ↓
构造 messages
  ↓
调用模型
  ↓
校验模型输出
  ↓
记录日志
  ↓
返回答案
```

核心区别是：**AI Gateway 不是简单代理模型 API，而是要把模型的不确定输出变成稳定的软件接口。**
