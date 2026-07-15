# 显式 Provider 降级链

fallback_router.py

```py
from __future__ import annotations

from llm_api_demo.exceptions import AllProvidersFailedException, LlmProviderException
from llm_api_demo.provider_clients import LlmProviderClient
from llm_api_demo.schemas import UnifiedChatRequest, UnifiedChatResponse


class ProviderFallbackRouter:
    """显式 Provider 降级链。"""

    def __init__(self, clients: list[LlmProviderClient]) -> None:
        self.clients = clients  # 按优先级排序的 provider client 列表。

    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        """异步依次尝试 provider，成功则返回，临时性失败则降级。"""
        failures: list[LlmProviderException] = []

        for client in self.clients:
            try:
                return await client.chat(request)
            except LlmProviderException as exc:
                failures.append(exc)

                if not self._should_fallback(exc):
                    raise

        raise AllProvidersFailedException(failures)

    @staticmethod
    def _should_fallback(exc: LlmProviderException) -> bool:
        """只对限流、5xx、超时、网络错误降级。"""
        return exc.status_code in {429, 500, 502, 503, 504, -1}

```
