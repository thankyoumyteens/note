# llm_clients.py

```python
from __future__ import annotations

from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from llm_api_demo.schemas import StreamChatRequest
from llm_api_demo.settings import settings


class LlmStreamRouter:
    """根据 provider 路由到 OpenAI / DeepSeek / Claude。"""

    def __init__(self) -> None:
        self._openai_client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

        self._deepseek_client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

        self._claude_client = AsyncAnthropic(
            api_key=settings.anthropic_api_key,
            base_url=settings.anthropic_base_url,
        )

    async def stream(self, request: StreamChatRequest) -> AsyncIterator[str]:
        """统一返回文本 chunk，不把 provider 原始流式事件暴露给 Controller。"""

        match request.provider:
            case "openai":
                async for chunk in self._stream_openai(request):
                    yield chunk

            case "deepseek":
                async for chunk in self._stream_deepseek(request):
                    yield chunk

            case "claude":
                async for chunk in self._stream_claude(request):
                    yield chunk

            case _:
                raise ValueError(f"Unsupported provider: {request.provider}")

    async def _stream_openai(self, request: StreamChatRequest) -> AsyncIterator[str]:
        """OpenAI Chat Completions streaming。"""

        stream = await self._openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=self._build_openai_messages(request),
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            stream=True,
        )

        async for event in stream:
            if not event.choices:
                continue

            content = event.choices[0].delta.content

            if content:
                yield content

    async def _stream_deepseek(self, request: StreamChatRequest) -> AsyncIterator[str]:
        """DeepSeek 使用 OpenAI-compatible Chat Completions streaming。"""

        stream = await self._deepseek_client.chat.completions.create(
            model=settings.deepseek_model,
            messages=self._build_openai_messages(request),
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            stream=True,
        )

        async for event in stream:
            if not event.choices:
                continue

            content = event.choices[0].delta.content

            if content:
                yield content

    async def _stream_claude(self, request: StreamChatRequest) -> AsyncIterator[str]:
        """Claude Messages API streaming。"""

        stream = await self._claude_client.messages.create(
            model=settings.claude_model,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            system=request.system,
            messages=[
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            stream=True,
        )

        async for event in stream:
            if event.type != "content_block_delta":
                continue

            delta = event.delta

            if getattr(delta, "type", None) != "text_delta":
                continue

            text = getattr(delta, "text", None)

            if text:
                yield text

    def _build_openai_messages(self, request: StreamChatRequest) -> list[dict[str, str]]:
        """构造 OpenAI-compatible messages。"""

        messages: list[dict[str, str]] = []

        if request.system and request.system.strip():
            messages.append(
                {
                    "role": "system",
                    "content": request.system,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.message,
            }
        )

        return messages
```

这里做了统一抽象：

```text
OpenAI / DeepSeek 原始流：
choices[0].delta.content

Claude 原始流：
content_block_delta → delta.text

Controller 拿到的统一结果：
AsyncIterator[str]
```

也就是说，Controller 不关心底层 provider 的 streaming 格式。
