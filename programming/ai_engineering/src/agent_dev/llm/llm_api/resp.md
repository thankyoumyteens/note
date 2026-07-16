# 返回格式说明

响应示例中的模型名只用于展示字段含义。

大模型接口的返回结果，不只是“模型回答文本”。一个完整响应通常包含：

1. 请求 ID
2. 模型名称
3. 生成结果
4. 停止原因
5. token 用量
6. 工具调用信息
7. 错误信息
8. 流式输出 chunk

## OpenAI-compatible Chat Completions 返回格式

OpenAI / Qwen / DeepSeek 这类兼容 `/chat/completions` 的接口，通常返回类似结构：

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1718345013,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "RAG 是检索增强生成，用外部知识库增强大模型回答。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 35,
    "total_tokens": 155
  }
}
```

### id

表示这次模型响应的唯一 ID。

```json
"id": "chatcmpl-xxx"
```

用途：

1. 日志追踪
2. 问题排查
3. 调用链关联
4. 和供应商客服排查问题

生产系统里建议把它记录到日志里。

### object

表示响应对象类型。

普通非流式响应一般是：

```json
"object": "chat.completion"
```

流式 chunk 一般是：

```json
"object": "chat.completion.chunk"
```

它的作用是告诉你：这是完整响应，还是流式响应片段。

### created

表示响应创建时间，通常是 Unix 时间戳。

```json
"created": 1718345013
```

用途：

1. 记录请求时间
2. 排查延迟
3. 统计调用历史

### model

表示实际使用的模型。

```json
"model": "gpt-4o-mini"
```

注意：有些服务可能会做模型别名映射。比如你请求的是：

```json
"model": "qwen-plus"
```

返回里可能会告诉你实际命中的具体模型版本。

### choices

`choices` 是最核心字段，表示模型返回的候选结果列表。

```json
"choices": [
  {
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "这里是模型回答"
    },
    "finish_reason": "stop"
  }
]
```

普通业务里一般只取第一个：

```java
choices[0].message.content
```

### finish_reason

`finish_reason` 表示模型为什么停止输出。

常见值：

- stop = 正常停止
- length = 达到 max_tokens 或上下文长度限制
- tool_calls = 模型决定调用工具
- content_filter = 内容被安全策略过滤

工程上要特别关注：

```java
finish_reason = "length"
```

这说明回答可能被截断。这种情况下你不能直接认为回答完整，应该考虑：

1. 增大 max_tokens
2. 让模型继续生成
3. 缩短输入上下文
4. 分段处理任务

#### usage

`usage` 表示本次调用消耗了多少 token。

常见结构：

```json
{
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 35,
    "total_tokens": 155
  }
}
```

含义：

- prompt_tokens = 输入 token 数
- completion_tokens = 输出 token 数
- total_tokens = 总 token 数

这在生产系统里很重要，因为它直接关系到：

1. 成本统计
2. 用户额度
3. 限流策略
4. 性能分析
5. 上下文长度优化

## Responses API 返回格式

OpenAI 的 Responses API 和 Chat Completions 不一样。

Chat Completions 是：`choices[0].message.content`

Responses API 是：

1. `output[]` 里面找 type = message 的 item
2. 再从 `content[]` 里面找 type = output_text 的 text

一个简化版响应大概是：

```json
{
  "id": "resp_xxx",
  "object": "response",
  "created_at": 1718345013,
  "model": "gpt-5.5",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "RAG 是检索增强生成。"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 100,
    "output_tokens": 30,
    "total_tokens": 130
  }
}
```

其中 `content` 是数组，文本输出块的类型是 `output_text`，文本在 `text` 字段里；它也可能返回 `refusal` 类型的内容块。

## Claude Messages API 返回格式

Claude 的返回格式也不同。

典型响应：

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello!"
    }
  ],
  "model": "claude-opus-4-8",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 6
  }
}
```

### stop_reason

Claude 不叫 `finish_reason`，而叫 `stop_reason`。

常见值：

- end_turn = 正常结束
- max_tokens = 达到输出 token 限制
- stop_sequence = 遇到自定义停止序列
- tool_use = 模型请求调用工具
- model_context_window_exceeded = 上下文窗口超限
- refusal = 安全拒绝

## Error 错误返回格式

错误响应一般不是 `choices`。

例如：

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "param": null,
    "code": "invalid_api_key"
  }
}
```

常见错误类型：

- 400 = 请求参数错误
- 401 = API Key 错误
- 403 = 权限不足
- 404 = endpoint 或模型不存在
- 429 = 限流
- 500 = 服务端错误
- 503 = 服务不可用
