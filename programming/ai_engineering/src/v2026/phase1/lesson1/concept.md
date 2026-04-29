# 你需要先掌握的 5 个核心概念

## 1. Model Provider

模型供应商，例如：

```text
OpenAI
Anthropic
Google Gemini
DeepSeek
Qwen
Moonshot
```

在工程里不要把业务代码和某个供应商强绑定。

**错误做法：**

```java
OpenAiService.call(...)
```

**更好的抽象：**

```java
AiModelClient.generate(...)
```

后面你可以替换底层模型，而业务代码不用大改。

---

## 2. Model

同一个供应商下面会有不同模型。

例如：

```text
高质量模型：适合复杂推理、Agent、代码分析
低成本模型：适合分类、抽取、简单问答
多模态模型：适合图片、文档、截图理解
embedding 模型：适合 RAG 检索
rerank 模型：适合重排序
```

工程上你不能所有任务都用最贵的模型。后面要做：

```text
简单任务 -> 便宜模型
复杂任务 -> 强模型
失败重试 -> fallback 模型
批处理任务 -> 低成本模型
```

---

## 3. Message

普通聊天不是直接传一个字符串，而是传一组消息。

典型结构：

```json
[
  {
    "role": "system",
    "content": "你是一个企业知识库助手。"
  },
  {
    "role": "user",
    "content": "帮我总结这份文档。"
  }
]
```

**常见 role：**

```text
system：系统规则
user：用户输入
assistant：模型之前的回答
tool：工具调用结果
```

你要记住：

> AI 应用开发的本质之一，是管理好 messages。

---

## 4. Structured Output

不要让模型随便返回自然语言。

错误做法：

```text
请返回 JSON，格式如下……
```

更好的做法：

```text
使用 JSON Schema / DTO / 工具调用约束模型输出
```

例如你要做情绪分类，不应该让模型返回：

```text
这个用户好像有点生气，可能是负面情绪。
```

而应该返回：

```json
{
  "sentiment": "negative",
  "confidence": 0.91,
  "reason": "用户表达了明显不满"
}
```

这样 Java 后端才能稳定处理。

---

## 5. Tool Calling

Tool Calling 的意思是：模型不只是回答，还可以决定调用某个后端函数。

例如用户说：

```text
帮我查一下订单 123 的物流状态。
```

模型不能自己瞎编，它应该调用工具：

```json
{
  "toolName": "getOrderShippingStatus",
  "arguments": {
    "orderId": "123"
  }
}
```

然后你的 Java 后端真正去查数据库或调用 API。

这就是 Agent 的基础。
