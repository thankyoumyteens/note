# Spring Boot 的封装方式

不要在业务代码里到处写：

```java
WebClient.post()
```

更好的结构是：

```text
                    ┌──────────────┐
                    │  Controller  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LlmService  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LlmClient   │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
   ┌────────────────┐ ┌────────────┐ ┌──────────────┐
   │ OpenAI Client  │ │ClaudeClient│ │ OpenAI 兼容层 │
   └───────┬────────┘ └─────┬──────┘ └──────┬───────┘
           │                │               │
           ▼                ▼               ▼
      OpenAI API       Claude API     Qwen / DeepSeek API
```

先定义一个统一接口：

```java
public interface LlmClient {
    String chat(String provider, String userMessage);
}
```

业务层只关心：

```java
llmClient.chat("openai", "解释一下 RAG");
llmClient.chat("qwen", "解释一下 RAG");
llmClient.chat("deepseek", "解释一下 RAG");
llmClient.chat("claude", "解释一下 RAG");
```

底层再根据 provider 调不同 API。
