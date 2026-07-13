# 调用 OpenAI Responses API

Responses API 使用 `client.responses.create()` 创建模型响应；`input` 可以直接传字符串，等价于 user 文本输入；`instructions` 用于放入 system/developer 类指令；`max_output_tokens` 用于限制模型最多生成的 token 数。

开启流式输出时，请求里设置 `stream=True`，SDK 会逐个返回事件。真正的增量文本在 `response.output_text.delta` 事件的 `delta` 字段里。

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

# 发起 Responses API 流式请求。
stream = client.responses.create(
    model="gpt-4.1-mini",  # 要调用的模型名称
    instructions="你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",  # system / developer 类指令
    input="用一句话解释什么是 RAG。",  # 用户输入
    temperature=0.2,  # 控制模型输出随机性的参数
    max_output_tokens=1000,  # 限制模型最多生成的 token 数
    stream=True,  # 启用流式输出
)

print("AI 回答：")

for event in stream:
    # Responses API 的文本增量事件是 response.output_text.delta。
    if event.type != "response.output_text.delta":
        continue

    if event.delta:
        print(event.delta, end="", flush=True)

print()
```

## 运行

```bash
uv run python main.py
```
