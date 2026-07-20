# Spring AI

本实现基于前文的 [Spring AI Prompt 模板](../../prompt_template/spring_ai/spring_ai.md)。Spring AI 的 ProviderClient 已经把统一 `USER`、`ASSISTANT` 消息转换为对应的 `UserMessage`、`AssistantMessage`，因此不需要绕过现有 Router 直接调用 `ChatClient`。

`PromptTemplate` 继续渲染 system 和当前 user 消息；固定 Few-shot 消息按顺序插入当前输入之前：

```text
VersionedPromptTemplate.render()
  -> 固定 UnifiedChatMessage 示例
  -> 当前 UnifiedChatMessage.user
  -> ProviderFallbackRouter
  -> SpringAiProviderClient
```

按照[配置 Few-shot 示例](./config.md)修改 `PromptConfig` 和 `IntentClassificationService`。ProviderClient、统一 DTO 和 Controller 保持不变。
