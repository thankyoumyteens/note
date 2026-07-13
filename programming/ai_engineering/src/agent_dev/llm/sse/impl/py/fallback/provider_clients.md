# ProviderClient

stream_provider_clients.py

```py
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from contextlib import aclosing

from anthropic import APIError as AnthropicAPIError
from anthropic import AsyncAnthropic
from openai import APIConnectionError, APIError, APITimeoutError, AsyncOpenAI

from llm_api_demo.exceptions import LlmProviderException
from llm_api_demo.provider_clients import should_retry_exception
from llm_api_demo.schemas import (
    ChatRole,
    LlmProvider,
    StreamEventType,
    UnifiedChatRequest,
    UnifiedChatStreamEvent,
)
from llm_api_demo.settings import settings


class LlmStreamProviderClient(ABC):
    """统一异步流式 ProviderClient 接口。"""

    @property
    @abstractmethod
    def provider(self) -> str:
        """返回 provider 名称。"""

    @abstractmethod
    def stream(self, request: UnifiedChatRequest) -> AsyncIterator[UnifiedChatStreamEvent]:
        """发起异步流式请求。"""


class OpenAiCompatibleStreamProviderClient(LlmStreamProviderClient):
    """OpenAI-compatible 异步流式 ProviderClient。"""

    def __init__(self, provider: LlmProvider, api_key: str, base_url: str, model: str) -> None:
        self._provider = provider  # provider 枚举。
        self._model = model  # 模型名称。
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=settings.request_timeout_seconds,
        )  # 异步 SDK 客户端。

    @property
    def provider(self) -> str:
        return self._provider.value

    async def stream(self, request: UnifiedChatRequest) -> AsyncIterator[UnifiedChatStreamEvent]:
        """当前 provider 内部重试；已经输出内容后不再重试。"""
        last_error: LlmProviderException | None = None  # 最后一次 provider 异常。

        for attempt in range(settings.max_retries + 1):
            content_started = False  # 当前尝试是否已经输出过内容。

            try:
                # 外层生成器被关闭时，继续关闭当前单次调用生成器。
                async with aclosing(self._stream_once(request)) as provider_stream:
                    async for event in provider_stream:
                        if event.type == StreamEventType.MESSAGE:
                            content_started = True

                        yield event

                return

            except LlmProviderException as exc:
                last_error = exc

                # 已经输出过内容，不能 retry，否则前端可能收到重复文本。
                if content_started:
                    raise

                # 参数、认证、权限等非临时错误不重试。
                if not should_retry_exception(exc):
                    raise

                # 达到最大重试次数后，把异常交给 fallback router。
                if attempt >= settings.max_retries:
                    raise

        if last_error:
            raise last_error

    async def _stream_once(self, request: UnifiedChatRequest) -> AsyncIterator[UnifiedChatStreamEvent]:
        """执行一次 OpenAI-compatible 异步 streaming 请求。"""
        try:
            messages = [{"role": "system", "content": request.system}]  # OpenAI-compatible 消息列表。

            for message in request.messages:
                messages.append({"role": message.role.value, "content": message.content})

            stream = await self.client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=request.options.temperature,
                max_tokens=request.options.max_tokens,
                top_p=request.options.top_p,
                stream=True,
            )

            # 正常完成、异常或任务取消时都关闭上游 HTTP stream。
            async with stream:
                async for chunk in stream:
                    if not chunk.choices:
                        continue

                    content = chunk.choices[0].delta.content

                    if content:
                        yield UnifiedChatStreamEvent(
                            type=StreamEventType.MESSAGE,
                            provider=self._provider,
                            model=chunk.model or self._model,
                            content=content,
                        )

        except (APITimeoutError, APIConnectionError) as exc:
            raise LlmProviderException(
                self.provider,
                -1,
                f"{self.provider} timeout or connection error",
            ) from exc
        except APIError as exc:
            raise LlmProviderException(
                self.provider,
                getattr(exc, "status_code", -1) or -1,
                str(exc),
                str(getattr(exc, "response", "")),
            ) from exc


class AnthropicStreamProviderClient(LlmStreamProviderClient):
    """Anthropic Messages API 异步流式 ProviderClient。"""

    def __init__(self) -> None:
        self.client = AsyncAnthropic(
            api_key=settings.anthropic_api_key,
            base_url=settings.anthropic_base_url,
            timeout=settings.request_timeout_seconds,
        )  # 异步 SDK 客户端。

    @property
    def provider(self) -> str:
        return LlmProvider.ANTHROPIC.value

    async def stream(self, request: UnifiedChatRequest) -> AsyncIterator[UnifiedChatStreamEvent]:
        """把 Anthropic content_block_delta 转成统一 MESSAGE 事件。"""
        try:
            messages = [
                {"role": message.role.value, "content": message.content}
                for message in request.messages
                if message.role in {ChatRole.USER, ChatRole.ASSISTANT}
            ]  # Anthropic messages 只放 user / assistant。

            stream = await self.client.messages.create(
                model=settings.anthropic_model,
                system=request.system,
                messages=messages,
                temperature=request.options.temperature,
                max_tokens=request.options.max_tokens,
                stream=True,
            )

            # 正常完成、异常或任务取消时都关闭上游 HTTP stream。
            async with stream:
                async for event in stream:
                    if event.type != "content_block_delta":
                        continue

                    delta = event.delta

                    if getattr(delta, "type", "") != "text_delta":
                        continue

                    text = getattr(delta, "text", "")

                    if text:
                        yield UnifiedChatStreamEvent(
                            type=StreamEventType.MESSAGE,
                            provider=LlmProvider.ANTHROPIC,
                            model=settings.anthropic_model,
                            content=text,
                        )

        except AnthropicAPIError as exc:
            raise LlmProviderException(
                self.provider,
                getattr(exc, "status_code", -1) or -1,
                str(exc),
            ) from exc
```
