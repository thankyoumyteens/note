# 调用 OpenAI Responses API

Responses API 使用 `client.responses.create()` 创建模型响应；`input` 可以直接传字符串，等价于 user 文本输入；`instructions` 用于放入 system/developer 类指令；`max_output_tokens` 用于限制模型最多生成的 token 数。

## 依赖

```bash
uv add openai
```

## 代码

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="换成你自己的KEY",
)

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",
    input="用一句话解释什么是 RAG。",
    temperature=0.2,
    max_output_tokens=1000,
)

content = response.output_text

if not content:
    raise RuntimeError("大模型没有返回文本内容")

print(content)
```

## 运行

```bash
uv run python main.py
```
