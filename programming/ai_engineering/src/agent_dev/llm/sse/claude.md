# Anthropic Messages API streaming 格式

Anthropic / Claude Messages API 的 streaming 事件更复杂，不只是 `delta.content`。

常见事件类型类似：

```text
message_start
content_block_start
content_block_delta
content_block_stop
message_delta
message_stop
ping
error
```

Anthropic Messages streaming 是通过 SSE 连续返回事件；客户端需要按 `event` 类型处理，并从 `data` 中提取增量内容。

典型流程：

```text
event: message_start
data: {...}

event: content_block_start
data: {...}

event: content_block_delta
data: {"delta":{"type":"text_delta","text":"你好"}}

event: content_block_delta
data: {"delta":{"type":"text_delta","text":"，"}}

event: content_block_stop
data: {...}

event: message_stop
data: {...}
```

你主要提取的是：

```text
content_block_delta.data.delta.text
```

所以 Anthropic-compatible streaming 和 OpenAI-compatible streaming 不能用同一个解析器。
