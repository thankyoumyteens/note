# 调用 OpenAI-compatible API

## 依赖

```bash
uv add openai
```

## 代码

```python
import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["LLM_API_KEY"],
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"),
)

response = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[
        {
            "role": "system",
            "content": "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",
        },
        {
            "role": "user",
            "content": "用一句话解释什么是 RAG。",
        },
    ],
    temperature=0.2,
    max_tokens=1000,
)

content = response.choices[0].message.content

if content is None:
    raise RuntimeError("大模型没有返回文本内容")

print(content)
```

## 运行

```bash
uv run python main.py
```
