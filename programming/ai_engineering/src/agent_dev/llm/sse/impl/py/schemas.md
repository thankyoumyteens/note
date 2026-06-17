# schemas.py

```python
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Provider = Literal["openai", "deepseek", "claude"]


class StreamChatRequest(BaseModel):
    """前端 POST SSE 请求体。"""

    provider: Provider
    message: str = Field(min_length=1)
    system: str | None = None
```

目前只支持：

```text
openai
deepseek
claude
```
