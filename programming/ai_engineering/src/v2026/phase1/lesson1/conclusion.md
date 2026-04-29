# 这一课你要真正理解的点

你现在不是为了写出复杂功能，而是先建立一个可扩展架构：

```text
Controller 不直接调用模型
Service 不关心具体供应商
LlmClient 是抽象接口
具体模型供应商只是实现类
```

这样后面你可以接：

```text
OpenAI
Claude
Gemini
DeepSeek
Qwen
本地模型
公司内部模型网关
```

业务层不用重写。
