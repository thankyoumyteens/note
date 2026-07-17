# WebClient

WebClient 本身不提供 Prompt 模板抽象，因此在现有统一模型调用链前增加模板渲染层：

```text
业务输入
  -> PromptTemplate
  -> PromptRenderer
  -> RenderedPrompt
  -> UnifiedChatRequest
  -> ProviderFallbackRouter
```

本实现复用前文的 `UnifiedChatRequest`、`UnifiedChatResponse` 和 `ProviderFallbackRouter`，不修改 ProviderClient、超时、重试和降级逻辑。

模板层只负责生成最终消息。模型输出的 JSON 解析、Schema 校验和业务校验属于后续结构化输出章节。
