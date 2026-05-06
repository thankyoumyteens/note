# 核心概念

## 什么是 OpenAI-compatible API？

很多模型供应商都兼容 OpenAI 的 Chat Completions API 格式。

例如：

```http
POST /v1/chat/completions
```

请求体通常类似：

```json
{
  "model": "xxx",
  "messages": [
    {
      "role": "system",
      "content": "你是一个严谨、简洁的助手。"
    },
    {
      "role": "user",
      "content": "请解释什么是 RAG。"
    }
  ],
  "temperature": 0.3
}
```

这样做的好处是：

- 同一套调用格式可以兼容多个模型供应商
- 后端只需要修改 `base-url`、`api-key`、`model`
- 后续可以做多模型切换和 fallback

常见 OpenAI-compatible 供应商包括：

- OpenAI
- DeepSeek
- Qwen
- Moonshot
- 部分企业内部模型网关

**注意：**

```text
OpenAI-compatible 不代表 100% 兼容。
```

不同供应商可能在以下方面不同：

- base URL
- 模型名称
- streaming 格式
- function calling 支持程度
- response_format 支持程度
- 错误响应格式

---

## 什么是 Chat Completions？

Chat Completions 是一种对话式模型调用格式。

它的核心不是传一个字符串，而是传一组消息：

```json
[
  {
    "role": "system",
    "content": "你是一个助手。"
  },
  {
    "role": "user",
    "content": "什么是 RAG？"
  }
]
```

模型根据这组消息生成下一条 assistant 回复。

你可以理解为：

```text
messages = 当前对话上下文
```

---

## messages 和 role

### 1. `system`

系统规则，用来约束模型整体行为。

例如：

```json
{
  "role": "system",
  "content": "你是一个严谨、简洁的 AI 应用开发助手。"
}
```

作用：

- 定义模型身份
- 定义回答风格
- 定义输出要求
- 定义任务边界

---

### 2. `user`

用户的输入。

例如：

```json
{
  "role": "user",
  "content": "请用三句话解释什么是 RAG。"
}
```

---

### 3. `assistant`

大模型的历史回复。

多轮对话时会用到。

例如：

```json
{
  "role": "assistant",
  "content": "RAG 是检索增强生成..."
}
```

---

### 4. `tool`

工具调用结果。

后续 Function Calling / Tool Calling 会用到。

例如：

```json
{
  "role": "tool",
  "content": "订单 10086 当前状态：已发货。"
}
```

---

## 为什么 system prompt 很重要？

`system prompt` 是模型行为的上层约束。

例如：

```text
你是一个严谨、简洁的 AI 应用开发助手。
```

它会影响：

- 回答是否简洁
- 是否使用某种格式
- 是否输出 JSON
- 是否遵守某些限制
- 是否拒绝越界任务

在 AI 应用开发中，`system prompt` 经常用于定义：

```text
这个模型调用节点的职责是什么。
```

例如：

- 聊天助手
- JSON 抽取器
- SQL 生成器
- 工具选择器
- RAG 回答器
- JSON 修复器

## 什么是 temperature？

`temperature` 用来控制模型输出的随机性。

一般理解：

```text
temperature 越低，输出越稳定。
temperature 越高，输出越发散。
```

常见取值：

| 场景       | 推荐 temperature |
| ---------- | ---------------- |
| 结构化输出 | 0 ~ 0.2          |
| 信息抽取   | 0 ~ 0.2          |
| RAG 问答   | 0.1 ~ 0.4        |
| 代码生成   | 0.1 ~ 0.4        |
| 创意写作   | 0.7 ~ 1.0        |
