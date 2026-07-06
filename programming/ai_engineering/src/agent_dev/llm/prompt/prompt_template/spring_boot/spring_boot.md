# 实现 Prompt 模板设计

实现 Prompt 模板设计，核心不是把 prompt 字符串直接写进调用代码里，而是把它拆成：

```
PromptTemplate
  ↓
PromptRenderer
  ↓
RenderedPrompt
  ↓
WebClient 调用 LLM
```

也就是：

```
业务输入
  ↓
填充 Prompt 模板变量
  ↓
生成 system / user messages
  ↓
WebClient 调用 OpenAI-compatible API
  ↓
返回模型结果
```
