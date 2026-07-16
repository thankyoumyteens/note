# 请求参数说明

文中的模型名只用于说明配置方式，运行时应替换为 Provider 当前可用的模型 ID。

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
  "max_tokens": 1000,
  "stream": false
}
```

可以先这样理解：

- model = 用哪个模型
- messages = 给模型看的上下文
- temperature = 回答随机性 / 稳定性
- max_tokens = 最多生成多少 token
- stream = 一次性返回完整响应，还是边生成边返回

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

## stream：是否使用流式响应

`stream` 决定模型响应是一次性返回，还是在生成过程中分批返回。

### stream=false

`stream=false` 表示使用非流式响应：

1. 客户端发送请求。
2. Provider 等模型生成完成。
3. Provider 返回一个完整的响应对象。
4. 客户端从完整响应中读取文本、停止原因和 Token usage。

这种模式的响应边界清晰，可以直接映射为普通的统一响应 DTO，适合先学习模型调用、参数映射、错误处理、重试和 Provider 降级。

阶段一的示例以非流式调用为主，因此建议显式使用：

```json
{
  "stream": false
}
```

### stream=true

`stream=true` 表示使用流式响应：

1. 客户端发送请求。
2. Provider 在生成过程中持续返回事件或数据块。
3. 客户端逐个解析并处理这些事件。
4. 收到结束事件后，本次响应才算完成。

```json
{
  "stream": true
}
```

流式响应不是一个普通响应对象，而是一段随时间到达的事件序列。不同事件可能分别携带：

- 增量文本
- 响应标识和模型信息
- 停止原因
- Token usage
- 错误信息
- 结束标记

因此，`stream=true` 的响应不能直接反序列化为非流式调用使用的普通响应 DTO。客户端需要持续读取事件，并根据 Provider 的事件协议提取和组合信息。

## 两种模式的响应结构差异

| 对比项 | `stream=false` | `stream=true` |
| --- | --- | --- |
| 返回方式 | 生成完成后一次性返回 | 生成过程中分批返回 |
| 响应结构 | 一个完整响应对象 | 多个事件或数据块组成的序列 |
| 文本内容 | 通常位于一个完整字段中 | 分散在多个增量事件中 |
| 停止原因 | 通常随完整响应返回 | 通常在接近结束的事件中返回 |
| Token usage | 通常从完整响应读取 | 可能只在结束阶段返回，也可能需要额外配置 |
| 客户端处理 | 读取并映射一个 DTO | 持续解析、转换和转发事件 |

`stream=true` 只是表示上游模型 API 使用流式响应，不等同于 SSE。Streaming 描述数据逐步返回的方式，SSE 是服务端向客户端推送事件的一种传输格式。

阶段一只需要理解 `stream` 参数和两种响应结构的差异。具体的 OpenAI-compatible、Responses API、Anthropic Messages API 事件格式，以及 Spring Boot + WebClient、Spring AI、Python 的流式实现，统一放在阶段四的[什么是 Streaming](../sse/streaming.md)及其后续章节中。
