# 调用 Anthropic Messages API

Anthropic 官方 Python SDK 使用 `Anthropic` 客户端，通过 `client.messages.create()` 调用 Messages API；请求里使用 `system` 放系统指令，`messages` 放 user / assistant 对话消息，`max_tokens` 限制最大输出 token。

## 依赖

```bash
uv add anthropic
```

## 代码

```python
import os

from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.getenv("LLM_BASE_URL", "https://api.anthropic.com"),
)

response = client.messages.create(
    model=os.environ["LLM_MODEL"],
    system="你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",
    messages=[
        {
            "role": "user",
            "content": "用一句话解释什么是 RAG。",
        }
    ],
    temperature=0.2,
    max_tokens=1000,
)

texts = []

for block in response.content:
    if block.type == "text":
        texts.append(block.text)

content = "".join(texts)

if not content:
    raise RuntimeError("大模型没有返回文本内容")

print(content)
```

## 运行

```bash
uv run python main.py
```
