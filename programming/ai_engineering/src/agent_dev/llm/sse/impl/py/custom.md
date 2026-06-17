# 如果前端想要 JSON data 格式

如果前端后续要求这种格式：

```text
event:message
data:{"content":"检索增强生成"}
```

只需要改 `sse_event`，让 data 支持对象并用 `json.dumps` 序列化：

```python
import json
from typing import Any


def sse_event(event: str, data: Any) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"event:{event}\ndata:{payload}\n\n"
```

然后在 `main.py` 里改成：

```python
yield sse_event("message", {"content": chunk})
yield sse_event("done", {"done": True})
```

错误事件：

```python
yield sse_event("error", {"message": to_safe_error_message(exc)})
```

这样前端收到的就是：

```text
event:message
data:{"content":"检索增强生成"}

event:done
data:{"done":true}
```
