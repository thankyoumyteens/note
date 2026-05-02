# 关于 OpenAI Responses API

上面为了兼容大多数供应商，使用的是 `/v1/chat/completions`。

但如果你明确使用 OpenAI 官方新接口，可以改成 Responses API。OpenAI 官方文档建议新项目优先使用 Responses API，因为它支持更丰富的 agentic 能力，包括内置工具、结构化输出、函数调用和多模态输入。

Responses API 的请求结构大致是：

```json
{
  "model": "gpt-5.1-mini",
  "input": "请用三句话解释什么是 RAG。"
}
```

但这一阶段我建议你先用 OpenAI-compatible 版本。原因很简单：

```text
兼容供应商更多
迁移到国产模型更方便
容易理解底层调用
后面接 Spring AI 也更顺
```
