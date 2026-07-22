# Spring AI

本实现复用前文的 `VersionedPromptTemplate`、统一 DTO、`SpringAiProviderClient` 和 `ProviderFallbackRouter`。Registry 保存完整 Prompt 版本，Spring AI 仍只负责模板渲染和最终模型调用。

```text
PromptSelection
  -> PromptRegistry.require()
  -> VersionedPromptTemplate.render()
  -> 版本内 Few-shot 消息
  -> ProviderFallbackRouter
```

按下面顺序实现：

1. [PromptRegistry](./registry.md)：定义完整版本、启用版本和注册表。
2. [配置 Prompt 版本](./config.md)：注册 `v1`、`v2` 并读取启用版本。
3. [IntentClassificationService](./service.md)：组装版本对应的消息并记录实际版本。

Controller 和同步 Provider 调用链保持不变。
