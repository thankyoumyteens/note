# 最小 LLM 应用

### 学习目标

理解模型能力边界，完成稳定、可配置的模型调用，为后续能力建立统一的调用基础。

### 需要掌握

- LLM 基本原理、擅长与不擅长的任务
- OpenAI-compatible API、OpenAI Responses API、Anthropic Messages API
- OpenAI、DeepSeek、Claude 等 provider 的接口差异
- model、messages、temperature、max_tokens、stream 等请求参数
- system、user、assistant 消息结构
- API Key、Base URL 和模型名的安全配置
- 统一请求、统一响应和统一 ProviderClient 抽象
- 400、401、403、429、5xx 等错误的分类处理
- 连接超时、响应超时、重试、fallback 和显式 provider 降级
- Token usage、响应延迟和调用结果的基础记录

### 实现路线

- Spring Boot + WebClient：理解底层 HTTP 协议、provider 差异和错误处理
- Spring AI：理解 Java 生态中的高层模型抽象
- Python + uv：完成轻量实验和后续评估工具准备

### 阶段产出与验收

- 同一个请求可以通过统一入口调用至少两类 provider
- 密钥与环境配置不写死在代码中，也不进入日志
- 能区分可重试错误与不可重试错误，并说明降级发生的条件
- 能记录 provider、模型、Token 用量、延迟和最终结果
