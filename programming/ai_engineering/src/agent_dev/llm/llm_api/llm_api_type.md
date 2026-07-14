# API 类型

阶段一主要涉及三类 API：

1. OpenAI-compatible Chat Completions API
2. OpenAI Responses API
3. Anthropic Messages API

这三类 API 都可以完成文本生成，但它们的 endpoint、鉴权方式、请求字段、响应结构和错误类型并不相同。

## 模型能力差异与 API 契约差异

模型能力差异和 Provider API 契约差异是两个不同问题。

模型能力差异关注模型本身，例如：

- 推理和代码能力
- 中文能力
- 上下文窗口
- 多模态能力
- Structured Outputs 和 Tool Calling 支持情况
- 延迟和成本

API 契约差异关注应用如何调用模型，例如：

- 请求发送到哪个 endpoint
- 使用哪个鉴权 Header
- system 指令放在哪个字段
- 输入消息如何组织
- 从响应的哪个字段读取文本
- 如何读取停止原因和 Token usage
- HTTP 错误会被 SDK 转换成什么异常

同一个模型可能通过不同 API 暴露，不同模型也可能使用相同的 OpenAI-compatible 契约。因此，不能根据模型名称推断完整的 API 请求和响应格式。

## 1. OpenAI-compatible Chat Completions API

OpenAI、Qwen、DeepSeek 等 Provider 都可以提供类似 Chat Completions 的接口：

```http
POST {baseUrl}/chat/completions
Authorization: Bearer API_KEY
Content-Type: application/json
```

请求体大致如下：

```json
{
  "model": "xxx",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "temperature": 0.2,
  "max_tokens": 1000,
  "stream": false
}
```

非流式响应的文本通常位于 `choices[0].message.content`，停止原因位于 `choices[0].finish_reason`，Token usage 使用 `prompt_tokens`、`completion_tokens` 和 `total_tokens`。

OpenAI-compatible 表示接口形状大致兼容，不表示所有 Provider 的字段、模型能力、错误码、扩展参数和边界行为完全一致。接入具体 Provider 时仍需以其文档为准。

如果需要用一套基础协议统一接入 OpenAI、Qwen、DeepSeek 等 Provider，Chat Completions 风格通常最容易抽象。

## 2. OpenAI Responses API

Responses API 是 OpenAI 面向文本、多模态和工具调用的新一代统一接口。

```http
POST {baseUrl}/responses
Authorization: Bearer API_KEY
Content-Type: application/json
```

请求体的核心字段是 `instructions` 和 `input`：

```json
{
  "model": "gpt-5.5",
  "instructions": "You are a helpful assistant.",
  "input": "Hello!",
  "max_output_tokens": 1000,
  "stream": false
}
```

Responses API 使用 `input` / `output`，而 Chat Completions 使用 `messages` / `choices`。

非流式响应需要从 `output` 数组中找到消息，再从消息的 `content` 数组中读取 `output_text`。SDK 通常还会提供 `output_text` 一类的便捷方法。停止状态由响应状态及输出内容共同表达，Token usage 使用 `input_tokens`、`output_tokens` 和 `total_tokens`。

Responses API 除了普通文本生成，还可以承载多模态输入、Structured Outputs、Function Calling 和内置工具，更适合后续 Agent、Tool Calling 和 Workflow 场景。普通聊天和多 Provider 兼容接入仍可使用 Chat Completions API。

## 3. Anthropic Messages API

Claude 原生 API 使用 Messages API，而不是 Chat Completions 格式：

```http
POST {baseUrl}/messages
x-api-key: API_KEY
anthropic-version: 2023-06-01
Content-Type: application/json
```

请求体大致如下：

```json
{
  "model": "claude-xxx",
  "max_tokens": 1000,
  "system": "You are a helpful assistant.",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "stream": false
}
```

Claude 的 system 指令是请求体中的独立字段，不是 `messages` 数组中的一条 system 消息。

非流式响应的文本位于 `content` 数组中的 `text` 内容块，停止原因使用 `stop_reason`，Token usage 使用 `input_tokens` 和 `output_tokens`。如果统一响应需要 `totalTokens`，可以在输入和输出 Token 都存在时计算得到。

## 三类 API 契约对照

| 对比项 | OpenAI-compatible Chat Completions | OpenAI Responses API | Anthropic Messages API |
| --- | --- | --- | --- |
| Endpoint | `{baseUrl}/chat/completions` | `{baseUrl}/responses` | `{baseUrl}/messages` |
| 鉴权 Header | `Authorization: Bearer ...` | `Authorization: Bearer ...` | `x-api-key: ...`，并携带 `anthropic-version` |
| system 表达 | `messages` 中的 system 消息 | `instructions` | 请求体顶层 `system` |
| 主要输入 | `messages` | `input` | `messages` |
| 最大输出 Token | `max_tokens` 或模型对应字段 | `max_output_tokens` | `max_tokens` |
| 返回文本 | `choices[0].message.content` | `output` 中的 `output_text` | `content` 中的 `text` 内容块 |
| 停止原因 | `finish_reason` | 响应状态和输出内容 | `stop_reason` |
| Token usage | `prompt_tokens`、`completion_tokens`、`total_tokens` | `input_tokens`、`output_tokens`、`total_tokens` | `input_tokens`、`output_tokens` |
| 错误表达 | HTTP 状态码和 `error` 响应体；不同兼容 Provider 可能有扩展 | HTTP 状态码和 Responses API 错误响应 | HTTP 状态码和 Anthropic 错误响应 |
| SDK 异常 | OpenAI SDK 或兼容 SDK 的状态码、连接、超时异常 | OpenAI SDK 的 Responses 调用异常 | Anthropic SDK 的状态码、连接、超时异常 |

参数名和错误结构可能随 Provider、模型和 SDK 版本变化。对照表描述的是当前项目需要统一处理的核心差异，具体字段仍以对应 Provider 文档和项目实际使用的 SDK 为准。

消息角色的详细含义见[system / user / assistant 消息结构](./message.md)，完整响应字段见[返回格式说明](./resp.md)。
