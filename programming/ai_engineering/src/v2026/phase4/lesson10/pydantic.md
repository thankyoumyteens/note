# Pydantic 结构化输出

Pydantic 是 Python 中非常常用的数据校验库。官方文档说明，Pydantic 使用 Python type hints 做数据验证；Pydantic 的“validation”是指实例化一个符合类型与约束的模型，如果数据无法解析成模型，会抛出 `ValidationError`。

你可以把它理解成 Python 版 DTO + 校验。

新建：

```text
python-tools/src/structured_output.py
```

代码：

````python
import json
import os
from enum import Enum

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError


load_dotenv()


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class TaskExtractionResult(BaseModel):
    task_name: str = Field(min_length=1)
    due_time_text: str | None = None
    priority: TaskPriority = TaskPriority.UNKNOWN
    assignee: str = Field(default="me", min_length=1)


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def cleanup_json(raw: str) -> str:
    text = raw.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    if text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    first = text.find("{")
    last = text.rfind("}")

    if first >= 0 and last > first:
        text = text[first:last + 1].strip()

    return text


def call_model_for_json(text: str) -> str:
    api_key = require_env("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    url = f"{base_url}/v1/chat/completions"

    system_prompt = """
你是一个任务信息抽取器。

你只能输出 JSON，不能输出 Markdown，不能输出解释。

JSON 字段要求：
{
  "task_name": "待办事项名称，字符串",
  "due_time_text": "原文中的时间表达，如果没有则为 null",
  "priority": "LOW | MEDIUM | HIGH | UNKNOWN",
  "assignee": "负责人。如果用户没有指定，则为 me"
}
""".strip()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
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

    return data["choices"][0]["message"]["content"]


def extract_task(text: str) -> TaskExtractionResult:
    raw = call_model_for_json(text)
    print("RAW:", raw)

    json_text = cleanup_json(raw)

    try:
        data = json.loads(json_text)
        return TaskExtractionResult.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Failed to parse structured output: {e}") from e


if __name__ == "__main__":
    result = extract_task("明天下午三点提醒我给张三发报价单，优先级高。")
    print(result)
    print(result.model_dump())
````

运行：

```bash
uv run python src/structured_output.py
```

预期输出类似：

```text
task_name='给张三发报价单' due_time_text='明天下午三点' priority=<TaskPriority.HIGH: 'HIGH'> assignee='me'
{'task_name': '给张三发报价单', 'due_time_text': '明天下午三点', 'priority': <TaskPriority.HIGH: 'HIGH'>, 'assignee': 'me'}
```

如果希望输出 JSON：

```python
print(result.model_dump_json(ensure_ascii=False, indent=2))
```
