# 调用 OpenAI-compatible API

OpenAI-compatible API 通常使用 Chat Completions 接口。开启流式输出时，请求里设置 `stream=True`，SDK 会逐个返回 chunk；真正的增量文本在 `choices[0].delta.content`。

## 依赖

```bash
uv add openai
```

## 代码

```python
from openai import OpenAI


client = OpenAI(
    api_key="换成你自己的KEY",
    base_url="https://api.deepseek.com",
)

# 发起 OpenAI-compatible 流式请求。
stream = client.chat.completions.create(
    model="deepseek-v4-pro",  # 要调用的模型名称
    messages=[  # 对话消息列表
        {
            "role": "system",  # 消息角色
            "content": "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",  # 消息内容
        },
        {
            "role": "user",  # 消息角色
            "content": "用一句话解释什么是 RAG。",  # 消息内容
        },
    ],
    temperature=0.2,  # 控制模型输出随机性的参数
    max_tokens=1000,  # 限制模型最多生成多少 token
    stream=True,  # 启用流式输出
)

print("AI 回答：")

for chunk in stream:
    if not chunk.choices:
        continue

    # 流式响应里读取 choices[0].delta.content，而不是 choices[0].message.content。
    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)

print()
```

## 运行

```bash
uv run python main.py
```
