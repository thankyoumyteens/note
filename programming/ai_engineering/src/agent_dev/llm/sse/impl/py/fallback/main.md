# main

sse_main.py

```py
from __future__ import annotations

import json
from dataclasses import asdict
from collections.abc import Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from llm_api_demo.exceptions import AllProvidersFailedException
from llm_api_demo.schemas import LlmProvider, StreamEventType, UnifiedChatRequest, UnifiedChatStreamEvent
from llm_api_demo.settings import settings
from llm_api_demo.stream_fallback_router import StreamProviderFallbackRouter
from llm_api_demo.stream_provider_clients import (
    AnthropicStreamProviderClient,
    LlmStreamProviderClient,
    OpenAiCompatibleStreamProviderClient,
)

app = FastAPI(title="LLM SSE Fallback Demo")


def build_stream_clients() -> list[LlmStreamProviderClient]:
    """根据 settings.provider_order 装配流式 provider clients。"""
    client_map: dict[str, LlmStreamProviderClient] = {
        "openai": OpenAiCompatibleStreamProviderClient(
            provider=LlmProvider.OPENAI,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            model=settings.openai_model,
        ),
        "deepseek": OpenAiCompatibleStreamProviderClient(
            provider=LlmProvider.DEEPSEEK,
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            model=settings.deepseek_model,
        ),
        "anthropic": AnthropicStreamProviderClient(),
    }

    return [client_map[name] for name in settings.provider_order]


router = StreamProviderFallbackRouter(build_stream_clients())


def sse_event(event: UnifiedChatStreamEvent) -> str:
    """把统一事件转换成 SSE 格式。"""
    data = json.dumps(asdict(event), ensure_ascii=False, default=str)
    return f"event:{event.type.value}\ndata:{data}\n\n"


@app.post("/api/ai/chat/stream")
def stream_chat(request: UnifiedChatRequest) -> StreamingResponse:
    """流式聊天接口。"""

    def event_generator() -> Iterator[str]:
        try:
            for event in router.stream(request):
                yield sse_event(event)

        except AllProvidersFailedException:
            yield sse_event(
                UnifiedChatStreamEvent(
                    type=StreamEventType.ERROR,
                    error_code="ALL_PROVIDERS_FAILED",
                    error_message="All providers failed",
                )
            )
            yield sse_event(UnifiedChatStreamEvent(type=StreamEventType.DONE))

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
```

## 运行

```sh
uv run uvicorn llm_api_demo.sse_main:app --reload --port 8000
```

## 测试请求

```sh
curl -N \
  -X POST http://127.0.0.1:8000/api/ai/chat/stream \
  -H 'Content-Type: application/json' \
  -d '{
    "system": "你是一个简洁的 AI Engineering 助手",
    "messages": [
      {
        "role": "user",
        "content": "解释一下 SSE fallback 为什么不能在输出一半后切 provider"
      }
    ],
    "options": {
      "temperature": 0.2,
      "max_tokens": 800
    }
  }'
```
