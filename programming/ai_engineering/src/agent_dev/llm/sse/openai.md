# OpenAI-compatible streaming 格式

OpenAI Chat Completions streaming 通常是这种：

请求：

```json
{
  "model": "qwen3.7-plus",
  "messages": [
    {
      "role": "user",
      "content": "解释一下 RAG"
    }
  ],
  "stream": true
}
```

响应片段类似：

```text
data: {"choices":[{"delta":{"content":"RAG"},"finish_reason":null}]}

data: {"choices":[{"delta":{"content":" 是"},"finish_reason":null}]}

data: {"choices":[{"delta":{"content":" 检索"},"finish_reason":null}]}

data: {"choices":[{"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

你要提取的是：

```text
choices[0].delta.content
```

而不是之前非流式时的：

```text
choices[0].message.content
```

## 非流式和流式的返回格式对比

非流式：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "完整答案"
      }
    }
  ]
}
```

流式：

```json
{
  "choices": [
    {
      "delta": {
        "content": "片段"
      }
    }
  ]
}
```
