# 调用 Anthropic Messages API

Anthropic 官方 Python SDK 使用 `Anthropic` 客户端，通过 `client.messages.create()` 调用 Messages API；请求里使用 `system` 放系统指令，`messages` 放 user / assistant 对话消息，`max_tokens` 限制最大输出 token。

开启流式输出时，请求里设置 `stream=True`。真正的文本增量通常在 `content_block_delta` 事件的 `delta.text` 字段里。

## 依赖

```bash
uv add anthropic
```

## 代码

```python
from anthropic import Anthropic


client = Anthropic(
    api_key="换成你自己的KEY",
    base_url="https://api.anthropic.com",
)

# 发起 Anthropic Messages API 流式请求。
stream = client.messages.create(
    model="claude-sonnet-4-6",  # 要调用的 Claude 模型名称
    system="你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",  # system 指令
    messages=[  # 对话消息列表
        {
            "role": "user",  # 消息角色
            "content": "用一句话解释什么是 RAG。",  # 消息内容
        }
    ],
    temperature=0.2,  # 控制模型输出随机性的参数
    max_tokens=1000,  # 限制模型最多生成多少 token
    stream=True,  # 启用流式输出
)

print("AI 回答：")

for event in stream:
    if event.type != "content_block_delta":
        continue

    delta = event.delta

    if getattr(delta, "type", None) != "text_delta":
        continue

    text = getattr(delta, "text", None)

    if text:
        print(text, end="", flush=True)

print()
```

## 运行

```bash
uv run python main.py
```
