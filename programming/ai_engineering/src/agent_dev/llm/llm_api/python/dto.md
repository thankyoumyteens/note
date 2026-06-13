# 统一结果对象和 Provider 枚举

编辑 clients.py：

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from anthropic import Anthropic, APIError as AnthropicAPIError
from openai import APIError as OpenAIAPIError
from openai import OpenAI

from llm_api_demo.settings import settings


class LlmProvider(StrEnum):
    """支持的模型服务商。"""

    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    CLAUDE = "claude"


@dataclass(frozen=True)
class LlmResult:
    """统一模型返回结果。"""

    provider: LlmProvider
    model: str
    content: str
```

## @dataclass 的作用

@dataclass 的作用是让一个类自动变成“数据对象”。

frozen=True 表示：对象创建后，字段不能再被修改。

@dataclass 会自动帮你生成这些方法：

```py
__init__
__repr__
__eq__
```

所以你可以直接这样创建对象：

```py
result = LlmResult(
    provider="qwen",
    model="qwen3.7-plus",
    content="RAG 是检索增强生成。"
)
```

不用自己写：

```py
class LlmResult:
    def __init__(self, provider, model, content):
        self.provider = provider
        self.model = model
        self.content = content
```
