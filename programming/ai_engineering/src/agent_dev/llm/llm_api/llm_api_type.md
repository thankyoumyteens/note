# API 类型

目前可以先分成两类。

## 1. OpenAI-compatible 接口

OpenAI、Qwen、DeepSeek 都可以用类似这种格式：

```http
POST {baseUrl}/chat/completions
Authorization: Bearer API_KEY
Content-Type: application/json
```

请求体大概是：

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

OpenAI 官方现在把 **Responses API** 作为主要接口，同时也说明 Chat Completions API 是之前的标准，并继续支持；如果要统一接 OpenAI / Qwen / DeepSeek，先用 Chat Completions 风格最容易。

## 2. Anthropic Messages API

Claude 原生 API 不是 Chat Completions 格式，而是 Messages API。Anthropic 官方 Java SDK 通过 `ANTHROPIC_API_KEY` 环境变量访问 Claude API，并提供 Messages API 客户端。

Claude 原生请求大概是：

```http
POST https://api.anthropic.com/v1/messages
x-api-key: ANTHROPIC_API_KEY
anthropic-version: 2023-06-01
Content-Type: application/json
```

请求体大概是：

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
  ]
}
```

注意：Claude 的 `system` 不是放在 `messages` 里的，而是一个单独字段。

## Responses API

Responses API 是 OpenAI 新一代文本/多模态/工具调用统一接口。

它可以理解成：Chat Completions API 的升级版 + Assistants API 的部分 Agent 能力 + 内置工具调用能力 + 更适合 Agent / Workflow / RAG / Tool Calling。

Responses API 是 Chat Completions 的演进版，并且推荐新项目优先使用 Responses API；Chat Completions 仍然继续支持。

### 它和 Chat Completions API 的核心区别

以前 Chat Completions 是这样：

```http
POST /v1/chat/completions
```

请求体核心是：

```json
{
  "model": "gpt-5.5",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Hello!" }
  ]
}
```

返回结果从这里取：

```java
choices[0].message.content
```

Responses API 是这样：

```http
POST /v1/responses
```

请求体核心是：

```json
{
  "model": "gpt-5.5",
  "instructions": "You are a helpful assistant.",
  "input": "Hello!"
}
```

返回结果从 `output` 数组里取文本，SDK 里也有 `output_text` 这类 helper。

Responses API 使用 `input` / `output`，而 Chat Completions 使用 `messages` / `choices`。

### 为什么 Agent 开发更适合 Responses API

Responses API 更适合 Agent，因为它不只是“聊天接口”。

它支持：

1. 普通文本生成
2. 多轮对话
3. 图片输入
4. Structured Outputs
5. Function Calling
6. Web Search
7. File Search
8. Computer Use
9. Code Interpreter
10. MCP

Responses API 是用于构建 agent-like applications 的统一接口，并支持 web search、file search、computer use、code interpreter、remote MCPs 等内置工具。

可以这样理解：

- Chat Completions API：适合普通聊天
- Responses API：适合 Agent / Tool Calling / Workflow / 多模态 / 状态管理
