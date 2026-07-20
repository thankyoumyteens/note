# WebClient

本实现基于前文的 [Prompt 模板设计](../../prompt_template/spring_boot/spring_boot.md)，不修改 `PromptTemplate`、`PromptRenderer`、统一 DTO、ProviderClient 和 Controller。

调用链只增加示例消息：

```text
system 模板
  -> Few-shot user / assistant 消息对
  -> 当前 user 消息
  -> UnifiedChatRequest
  -> ProviderFallbackRouter
```

按照[配置 Few-shot 示例](./config.md)修改 `PromptConfig` 和 `IntentClassificationService`。示例是应用维护的固定内容，不能从当前请求动态生成。
