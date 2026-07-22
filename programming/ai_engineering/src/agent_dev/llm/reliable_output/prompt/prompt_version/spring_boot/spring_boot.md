# WebClient

本实现基于前文 WebClient 版本的 Prompt 模板和 Few-shot 代码，引入一个进程内 `PromptRegistry`。一个 `PromptDefinition` 同时保存模板与配套示例，Service 根据应用配置精确取得当前版本。

```text
PromptSelection
  -> PromptRegistry.require()
  -> PromptDefinition
  -> PromptRenderer
  -> UnifiedChatRequest
  -> ProviderFallbackRouter
```

按下面顺序实现：

1. [PromptRegistry](./registry.md)：定义完整版本、启用版本和注册表。
2. [配置 Prompt 版本](./config.md)：同时注册 `v1`、`v2` 并读取启用版本。
3. [IntentClassificationService](./service.md)：解析版本、渲染并记录实际版本。

统一 DTO、ProviderClient、Router 和 Controller 保持不变。
