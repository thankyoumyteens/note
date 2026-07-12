# 显式 Provider 降级链

stream_fallback_router.py

```py
from __future__ import annotations

from collections.abc import Iterator

from llm_api_demo.exceptions import AllProvidersFailedException, LlmProviderException
from llm_api_demo.schemas import StreamEventType, UnifiedChatRequest, UnifiedChatStreamEvent
from llm_api_demo.stream_provider_clients import LlmStreamProviderClient


class StreamProviderFallbackRouter:
    """显式 Provider 流式降级链。"""

    def __init__(self, clients: list[LlmStreamProviderClient]) -> None:
        self.clients = clients  # 按优先级排序的 provider client 列表。

    def stream(self, request: UnifiedChatRequest) -> Iterator[UnifiedChatStreamEvent]:
        """只有当前 provider 尚未输出 message chunk 时，才允许 fallback。"""
        failures: list[LlmProviderException] = []  # provider 失败链路。

        for client in self.clients:
            content_started = False  # 当前 provider 是否已经输出过内容。

            try:
                for event in client.stream(request):
                    if event.type == StreamEventType.MESSAGE:
                        content_started = True

                    yield event

                yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
                return

            except Exception as exc:
                provider_exception = self._to_provider_exception(client.provider, exc)
                failures.append(provider_exception)

                # 已经输出过内容，不能切 provider。
                if content_started:
                    yield UnifiedChatStreamEvent(
                        type=StreamEventType.ERROR,
                        error_code="STREAM_INTERRUPTED",
                        error_message=provider_exception.message,
                    )
                    yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
                    return

                # 非临时错误不降级，避免掩盖参数、认证、权限问题。
                if not self._should_fallback(provider_exception):
                    yield UnifiedChatStreamEvent(
                        type=StreamEventType.ERROR,
                        error_code="PROVIDER_FAILED",
                        error_message=provider_exception.message,
                    )
                    yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
                    return

        raise AllProvidersFailedException(failures)

    @staticmethod
    def _should_fallback(exc: LlmProviderException) -> bool:
        """复用普通 API fallback 的临时错误判断。"""
        return exc.status_code in {429, 500, 502, 503, 504, -1}

    @staticmethod
    def _to_provider_exception(provider: str, exc: Exception) -> LlmProviderException:
        """把未知异常统一包装成 LlmProviderException。"""
        if isinstance(exc, LlmProviderException):
            return exc

        return LlmProviderException(
            provider=provider,
            status_code=-1,
            message=str(exc) or "Provider stream failed",
            response_body="",
        )
```
