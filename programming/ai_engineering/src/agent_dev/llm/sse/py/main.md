# main.py

```python
from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from llm_api_demo.llm_clients import LlmStreamRouter
from llm_api_demo.schemas import StreamChatRequest
from llm_api_demo.sse import sse_event

app = FastAPI(title="AI SSE Demo")

router = LlmStreamRouter()


@app.post("/api/ai/chat/stream")
async def stream_chat(request: StreamChatRequest) -> StreamingResponse:
    """
    POST SSE 流式聊天接口。

    前端使用 fetch + ReadableStream 接收。
    """

    async def event_generator() -> AsyncIterator[str]:
        try:
            async for chunk in router.stream(request):
                yield sse_event("message", chunk)

            yield sse_event("done", "[DONE]")

        except Exception as exc:
            yield sse_event("error", to_safe_error_message(exc))
            yield sse_event("done", "[DONE]")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


def to_safe_error_message(exc: Exception) -> str:
    """把异常转换成给前端看的错误信息。"""

    message = str(exc)

    if not message:
        return "AI streaming failed"

    return message
```

这个接口返回给前端的是：

```text
event:message
data:RAG

event:message
data: 是一种

event:message
data:检索增强生成

event:done
data:[DONE]
```
