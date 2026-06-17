# sse.py

```python
from __future__ import annotations


def sse_event(event: str, data: str) -> str:
    """
    把文本包装成 SSE 格式。

    输出示例：
    event:message
    data:hello

    """
    return f"event:{event}\ndata:{data}\n\n"
```

这个版本的前端会收到：

```text
event:message
data:RAG

event:message
data: 是一种

event:done
data:[DONE]
```
