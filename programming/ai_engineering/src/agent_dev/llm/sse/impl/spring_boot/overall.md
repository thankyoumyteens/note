# 总体架构

```text
                    ┌──────────────┐
                    │   Frontend   │
                    │ fetch stream │
                    └──────┬───────┘
                           │ POST text/event-stream
                           ▼
                    ┌──────────────┐
                    │  Controller  │
                    └──────┬───────┘
                           │ Flux<ServerSentEvent>
                           ▼
                    ┌──────────────┐
                    │ StreamRouter │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      OpenAI-compatible  Anthropic     Anthropic-compatible
      Stream Client      Stream Client Qwen Messages Client
             │             │             │
             ▼             ▼             ▼
      Qwen / DeepSeek   Claude API    Qwen Anthropic API
```

这里明确区分两类协议：

```text
OpenAI-compatible:
OpenAI / Qwen / DeepSeek
/v1/chat/completions
解析 choices[0].delta.content
```

```text
Anthropic Messages-compatible:
Claude / Qwen Anthropic-compatible
/v1/messages
解析 content_block_delta.data.delta.text
```
