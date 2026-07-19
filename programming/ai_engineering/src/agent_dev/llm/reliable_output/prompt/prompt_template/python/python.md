# Python + uv

Python 版本使用标准库 `string.Template` 实现变量渲染，不需要增加第三方依赖。

本实现继续使用订单意图识别案例，并复用前文 Python 版本的统一 DTO、异步 ProviderClient 和异步 `ProviderFallbackRouter`：

```text
业务输入
  -> PromptTemplate
  -> PromptRenderer
  -> RenderedPrompt
  -> UnifiedChatRequest
  -> await ProviderFallbackRouter.chat()
```

按下面的顺序实现：

1. [PromptTemplate 与 PromptRenderer](./template.md)：定义模板、校验变量并完成渲染。
2. [定义订单意图模板](./config.md)：集中保存模板内容和版本。
3. [IntentClassificationService](./service.md)：组装统一请求并异步调用 Router。
4. [FastAPI 使用方式](./main.md)：增加意图识别接口和测试请求。

模板渲染不执行 I/O，因此保持同步；Service、Router、ProviderClient 和 FastAPI endpoint 保持异步。
