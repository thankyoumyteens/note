# 统一 DTO

在 schemas.py 中追加：

```py
class StreamEventType(StrEnum):
    """统一流式事件类型。"""

    MESSAGE = "message"
    DONE = "done"
    ERROR = "error"


@dataclass(frozen=True)
class UnifiedChatStreamEvent:
    """统一流式响应事件。"""

    type: StreamEventType  # 事件类型。
    provider: LlmProvider | None = None  # 实际命中的 provider。
    model: str = ""  # 实际使用的模型。
    content: str = ""  # MESSAGE 事件里的增量文本。
    error_code: str = ""  # ERROR 事件里的错误码。
    error_message: str = ""  # ERROR 事件里的安全错误信息。
    metadata: dict[str, Any] = field(default_factory=dict)  # 扩展元数据。
```
