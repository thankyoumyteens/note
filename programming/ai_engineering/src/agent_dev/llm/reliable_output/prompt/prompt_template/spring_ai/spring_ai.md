# Spring AI

Spring AI 已提供 `PromptTemplate` 和变量渲染能力，因此不需要实现 WebClient 版本中的自定义 `PromptRenderer`。

本实现继续使用订单意图识别案例，并复用前文 Spring AI 版本的统一 DTO、`SpringAiProviderClient` 和 `ProviderFallbackRouter`：

```text
业务输入
  -> VersionedPromptTemplate
  -> Spring AI PromptTemplate.render()
  -> UnifiedChatRequest
  -> ProviderFallbackRouter
```

按下面的顺序实现：

1. [VersionedPromptTemplate](./template.md)：为 Spring AI 模板补充名称和版本。
2. [创建模板 Bean](./config.md)：集中定义 system、user 模板。
3. [IntentClassificationService](./service.md)：渲染变量并组装统一请求。
4. [Controller 使用方式](./controller.md)：接收业务输入并调用 Service。

这里只增加 Prompt 模板层，不修改 Spring AI ProviderClient 的超时、重试、降级和调用记录逻辑。
