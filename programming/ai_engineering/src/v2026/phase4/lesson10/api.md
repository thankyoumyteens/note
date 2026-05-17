# Python 调模型 API

新建：

```text
python-tools/src/call_model.py
```

代码：

```python
import os

import httpx
from dotenv import load_dotenv


load_dotenv()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def call_model(message: str) -> str:
    api_key = require_env("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    url = f"{base_url}/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一个严谨、简洁的 AI 应用开发助手。",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        "temperature": 0.1,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    answer = call_model("请用一句话解释什么是 RAG。")
    print(answer)
```

运行：

```bash
uv run python src/call_model.py
```

预期输出：

```text
RAG 是一种让大模型先检索外部知识，再基于检索结果生成回答的技术。
```
