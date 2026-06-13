# Spring AI

用 Spring AI 后，你不需要自己写 `WebClient.post()`、DTO、响应解析。

整体变成：

```text
                    ┌──────────────┐
                    │  Controller  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │AiChatService │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ChatClient  │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
   ┌────────────────┐ ┌────────────┐ ┌──────────────┐
   │ OpenAI Model   │ │Claude Model│ │OpenAI兼容模型 │
   └───────┬────────┘ └─────┬──────┘ └──────┬───────┘
           │                │               │
           ▼                ▼               ▼
      OpenAI API       Claude API     Qwen / DeepSeek API
```
