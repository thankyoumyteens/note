# 统一 ProviderClient

OpenAI-compatible Chat Completions、OpenAI Responses API 和 Anthropic Messages API 都能完成模型调用，但它们使用不同的 endpoint、鉴权方式、请求字段、响应结构和异常类型。

如果业务层直接调用这些 API，就必须知道每种协议的具体差异。例如，业务代码需要判断当前 Provider，再决定 system 指令放在 `messages`、`instructions` 还是请求体顶层，也需要从 `choices`、`output` 或 `content` 中提取文本。

Provider 增加以后，这些判断会散落在 Service、Controller 和重试降级逻辑中。业务层会同时承担业务处理和外部协议适配，修改一个 Provider 的请求格式也可能影响与它无关的代码。

ProviderClient 用于隔离这些变化。它是当前项目定义的内部抽象，不是 OpenAI、Anthropic、Spring AI 或某个 Python SDK 提供的统一类型。

## 所在位置

ProviderClient 位于统一业务调用与具体 Provider API 之间：

```text
Controller / Service
        ↓
Provider Router
        ↓
统一 ProviderClient 接口
        ↓
各 ProviderClient 实现
        ↓
Provider HTTP API 或 SDK
```

Controller 和 Service 使用统一请求与统一响应，不接触 Provider 的原始协议。Router 面向统一 ProviderClient 接口选择 Provider。每个具体 ProviderClient 只适配自己负责的 API。

## 统一接口的意义

统一 ProviderClient 接口通常只保留两类能力：

- 返回当前 Client 对应的 Provider 标识。
- 接收统一请求并返回统一响应。

业务层和 Router 因此不需要根据 Provider 类型调用不同的方法。增加新的 Provider 时，主要工作是增加一个实现，而不是在现有业务调用链中增加多处分支。

统一接口不要求所有 Provider 使用相同的底层技术。具体实现可以使用 WebClient、Spring AI ChatClient 或 Python SDK，只要对上层提供相同的请求、响应和异常语义。

## ProviderClient 的职责

每个具体 ProviderClient 负责：

1. 读取当前 Provider 的 Base URL、API Key、模型和超时配置。
2. 将统一请求转换成对应 API 的请求结构。
3. 使用正确的 endpoint 和鉴权方式调用 Provider。
4. 从 Provider 响应中提取文本、实际模型和停止原因。
5. 将不同格式的 Token usage 映射为统一结构。
6. 将 HTTP 错误、SDK 异常、超时和网络错误转换为统一 Provider 异常。

这些职责共同构成协议适配边界。ProviderClient 对上层隐藏外部契约差异，但不会改变 Provider 实际支持的模型能力。

## ProviderClient 不负责什么

ProviderClient 不负责：

- 决定业务场景应该使用哪个 Provider。
- 编排多个 Provider 的调用顺序。
- 在不同 Provider 之间执行降级。
- 处理 Controller 的 HTTP 请求和响应。
- 保存业务会话或执行 Agent 工作流。

单个 Provider 内部的超时和重试可以放在 ProviderClient 调用边界内，因为这些行为依赖当前 Provider 的配置和异常。跨 Provider 的切换由 Router 负责，避免协议适配和调用编排混在一起。

## 与统一 DTO 的关系

统一 DTO 定义应用内部希望使用的数据结构，ProviderClient 负责在统一 DTO 与 Provider 原始 DTO 之间转换。

请求方向：

```text
UnifiedChatRequest → Provider 原始请求
```

响应方向：

```text
Provider 原始响应 → UnifiedChatResponse
```

这种转换只统一不同 API 中含义相同的部分，例如消息、生成参数、文本、模型、停止原因和 Token usage。Provider 特有且无法合理统一的字段可以放在受控的 metadata 中，或者由专门能力单独建模，不应为了表面统一而丢失重要语义。

## 与 Router 的关系

ProviderClient 解决“怎样调用某一个 Provider”，Router 解决“这次应该按什么顺序调用哪些 Provider”。

当 ProviderClient 成功时，Router 直接返回统一响应。当 ProviderClient 抛出统一异常时，Router 根据错误类型决定立即结束，还是切换到下一个 Provider。

Router 不解析 Provider 原始响应，也不识别各 SDK 的异常类型。否则 Provider 契约差异会再次泄漏到统一调用层。

## 三种实现路线

三种实现路线使用相同的抽象目的，但底层适配方式不同：

- [Spring Boot + WebClient](./spring_boot/fallback/provider_interface.md)：各实现显式构造 HTTP 请求、解析响应并转换异常，最直接地体现 Provider API 契约差异。
- [Spring AI](./spring_ai/fallback/provider_interface.md)：使用 Spring AI 的模型抽象完成基础调用，再在 ProviderClient 中补齐统一 Provider、模型、Token usage 和异常语义。
- [Python + uv](./python/fallback/provider_clients.md)：使用对应的异步 SDK 调用 Provider，并在异步 ProviderClient 中完成统一 DTO 和异常转换。

三条路线中的具体接口和实现代码放在各自章节中，本章只说明 ProviderClient 在统一模型调用中的作用和边界。
