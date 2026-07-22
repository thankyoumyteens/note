# Python + uv

Python 版本在前文异步调用链前增加进程内 `PromptRegistry`。Registry 和模板渲染都是纯内存操作，保持同步；Service、Router、ProviderClient 和 FastAPI endpoint 继续异步。

```text
PromptSelection
  -> PromptRegistry.require()
  -> PromptRenderer.render()
  -> 版本内 Few-shot 消息
  -> await ProviderFallbackRouter.chat()
```

按下面顺序实现：

1. [PromptRegistry](./registry.md)：定义完整版本、启用版本和注册表。
2. [配置 Prompt 版本](./config.md)：注册 `v1`、`v2` 并从环境变量读取启用版本。
3. [IntentClassificationService](./service.md)：解析版本、异步调用 Router 并记录实际版本。

不增加第三方依赖，FastAPI 接口契约保持不变。
