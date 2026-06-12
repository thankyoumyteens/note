# 请求参数说明

调用 **Chat Completions 风格 API** 时最常见的基础参数：

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "你是一个 Java 后端助手。"
    },
    {
      "role": "user",
      "content": "解释一下 RAG。"
    }
  ],
  "temperature": 0.2,
  "max_tokens": 1000
}
```

可以先这样理解：

- model = 用哪个模型
- messages = 给模型看的上下文
- temperature = 回答随机性 / 稳定性
- max_tokens = 最多生成多少 token

## model：选择哪个模型

`model` 表示你要调用哪个大模型。

例如：

```json
{
  "model": "gpt-4o-mini"
}
```

或者：

```json
{
  "model": "qwen-plus"
}
```

或者：

```json
{
  "model": "deepseek-chat"
}
```

它决定了这次请求使用的模型能力。

不同模型通常差异在：

1. 推理能力
2. 代码能力
3. 中文能力
4. 多模态能力
5. 上下文窗口大小
6. 响应速度
7. 调用价格
8. 是否支持 Tool Calling
9. 是否支持 Structured Outputs

在工程上，`model` 不建议写死在业务代码里，而应该放到配置文件里。

例如：

```yaml
llm:
  providers:
    openai:
      model: gpt-4o-mini
    qwen:
      model: qwen-plus
    deepseek:
      model: deepseek-chat
```

这样以后换模型时，不需要改 Java 代码。

## messages：给模型看的对话上下文

`messages` 是 Chat Completions API 的核心参数。

它是一个数组，里面每一项代表一条消息：

```json
{
  "messages": [
    {
      "role": "system",
      "content": "你是一个 Java 后端助手。"
    },
    {
      "role": "user",
      "content": "解释一下 RAG。"
    }
  ]
}
```

每条消息通常包含两个字段：

- role = 这条消息是谁说的
- content = 这条消息的内容

常见的 role 有：

- system = 系统规则
- user = 用户输入
- assistant = 模型历史回复
- tool = 工具调用结果，后续 Tool Calling 会用到

## temperature：控制输出随机性

`temperature` 控制模型生成内容时的随机程度。

例如：

```json
{
  "temperature": 0.2
}
```

可以这样理解：

- temperature 越低 → 越稳定、越保守、越可控
- temperature 越高 → 越发散、越随机、越有创造性

常见取值：

| 场景              | 推荐 temperature |
| ----------------- | ---------------: |
| 代码生成          |        0.0 - 0.3 |
| RAG 问答          |        0.0 - 0.3 |
| Tool Calling      |        0.0 - 0.2 |
| JSON / 结构化输出 |        0.0 - 0.2 |
| 技术解释          |        0.2 - 0.5 |
| 文案生成          |        0.5 - 0.8 |
| 创意写作          |        0.7 - 1.0 |

对 Agent / RAG / Java 后端场景，建议默认：

```json
{
  "temperature": 0.2
}
```

原因是这些场景更需要：

- 稳定
- 准确
- 少幻觉
- 少乱发挥
- 格式可控

不太需要模型“自由创作”。

## max_tokens：限制最多生成多少 token

`max_tokens` 表示**最多允许模型生成多少 token**。

例如：

```json
{
  "max_tokens": 1000
}
```

注意：它限制的是**输出长度**，不是输入长度。

也就是说：

- messages 的长度 = 输入 token
- 模型生成的回答长度 = 输出 token
- max_tokens 控制的是输出 token 上限

在 Chat Completions 里，早期 / 非 reasoning 模型仍可用 `max_tokens`，reasoning 模型常用 `max_completion_tokens`，而 Responses API 用的是 `max_output_tokens`。

### 举例

如果你设置：

```json
{
  "max_tokens": 50
}
```

模型最多只生成大约 50 个 token，回答可能很短，甚至被截断。

如果你设置：

```json
{
  "max_tokens": 2000
}
```

模型可以生成更长回答，但成本和延迟也会增加。

### 常见建议

| 场景            |                   推荐 max_tokens |
| --------------- | --------------------------------: |
| 一句话解释      |                         100 - 200 |
| 普通问答        |                        500 - 1000 |
| 代码生成        |                       1000 - 3000 |
| 长文档总结      |                       2000 - 4000 |
| Agent 中间步骤  |                         300 - 800 |
| JSON 结构化输出 | 根据字段数量设置，通常 500 - 1500 |

如果你是普通 Spring Boot 聊天接口，入门可以先用：

```json
{
  "max_tokens": 1000
}
```
