# 多个 provider 下切换不同模型

核心原则：不要继续依赖 spring.ai.model.chat=openai / anthropic 这种单选自动配置。

改成：

1. 自己定义多个 ChatModel Bean
2. 自己定义多个 ChatClient Bean
3. 用 LlmRouterService 路由到不同 provider

最终架构

```text
                    ┌──────────────┐
                    │  Controller  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ LlmRouterSvc │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      openAiClient   qwenClient    claudeClient
             │             │             │
             ▼             ▼             ▼
        OpenAI API   DashScope API  Anthropic API
```

这里的重点是：

```text
OpenAI      → OpenAiChatModel
Qwen        → OpenAiChatModel，因为它走 OpenAI-compatible
Claude      → AnthropicChatModel
Router 层   → 根据 provider 选择 ChatClient
```
