# 创建 Pydantic 响应模型

用 Python DTO 校验 Java AI Gateway 返回的数据结构。

Pydantic 的 `BaseModel` 可以定义结构化数据模型；这和 Java 的 DTO 类似。Pydantic 官方文档说明，模型通常继承 `BaseModel` 并通过类型标注定义字段。

本课先对应三个 Java 接口：

```text
/api/ai/chat
/api/ai/extract-task
/api/ai/order-assistant
```

#### 代码

文件：

```text
python-tools/src/ai_gateway_tools/models.py
```

代码：

```python
from enum import Enum
from pydantic import BaseModel, Field


class TaskPriority(str, Enum):
    """对应 Java 里的 TaskPriority enum。"""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


class ChatResponse(BaseModel):
    """对应 POST /api/ai/chat 的响应。"""

    answer: str = Field(min_length=1)


class TaskExtractionResult(BaseModel):
    """对应 POST /api/ai/extract-task 的响应。"""

    taskName: str = Field(min_length=1)
    dueTimeText: str | None = None
    priority: TaskPriority
    assignee: str = Field(min_length=1)


class OrderAssistantResponse(BaseModel):
    """对应 POST /api/ai/order-assistant 的响应。"""

    answer: str = Field(min_length=1)
```

#### 代码说明

这里的 `TaskExtractionResult` 是 Python 侧 DTO，用于校验 Java 返回的 JSON 是否满足预期结构。

例如：

```text
priority 必须是 LOW / MEDIUM / HIGH / UNKNOWN
answer 不能为空
taskName 不能为空
```
