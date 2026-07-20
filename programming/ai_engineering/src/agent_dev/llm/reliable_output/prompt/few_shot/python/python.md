# Python + uv

本实现基于前文的 [Python Prompt 模板](../../prompt_template/python/python.md)，复用统一 DTO、异步 ProviderClient 和异步 `ProviderFallbackRouter`，不增加第三方依赖。

模板渲染和示例列表组装都是纯内存操作，保持同步；模型调用继续使用 `async def` 和 `await`：

```text
PromptRenderer.render()
  -> 固定 user / assistant 示例
  -> 当前 user 消息
  -> await ProviderFallbackRouter.chat()
```

按照[配置 Few-shot 示例](./config.md)修改 `prompts.py` 和 `intent_service.py`。`main.py`、统一 DTO 和 Provider 调用链保持不变。
