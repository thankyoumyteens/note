# 显式 Provider 降级链

fallback_router.py

```py
from __future__ import annotations

import logging

from dataclasses import replace
from datetime import UTC, datetime
from time import perf_counter
from typing import Protocol

from llm_api_demo.exceptions import AllProvidersFailedException, LlmProviderException
from llm_api_demo.provider_clients import LlmProviderClient
from llm_api_demo.schemas import (
    LlmCallRecord,
    LlmProvider,
    ProviderAttemptRecord,
    TokenUsage,
    UnifiedChatRequest,
    UnifiedChatResponse,
)

# 复用 Uvicorn 日志配置，确保记录器异常能够输出。
logger = logging.getLogger("uvicorn.error")


class LlmCallRecorder(Protocol):
    async def save(self, record: LlmCallRecord) -> None:
        """保存调用记录。"""


class ProviderFallbackRouter:
    """显式 Provider 降级链。"""

    def __init__(
        self,
        clients: list[LlmProviderClient],
        recorder: LlmCallRecorder,
    ) -> None:
        self.clients = clients  # 按优先级排序的 provider client 列表。
        self.recorder = recorder  # 调用记录器。

    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        """异步依次尝试 provider，成功则返回，临时性失败则降级。"""
        total_started = perf_counter()
        started_at = datetime.now(UTC)
        failures: list[LlmProviderException] = []
        attempts: list[ProviderAttemptRecord] = []

        for client in self.clients:
            provider_started = perf_counter()
            provider_started_at = datetime.now(UTC)

            try:
                response = await client.chat(request)
                provider_latency_ms = int((perf_counter() - provider_started) * 1000)
                total_latency_ms = int((perf_counter() - total_started) * 1000)
                attempts.append(self._success_attempt(
                    response, provider_started_at, provider_latency_ms
                ))

                result = replace(
                    response,
                    provider_latency_ms=provider_latency_ms,
                    total_latency_ms=total_latency_ms,
                )
                await self._save(self._success_record(request, started_at, result, attempts))
                return result
            except LlmProviderException as exc:
                failures.append(exc)
                attempts.append(self._failed_attempt(
                    client, exc, provider_started_at,
                    int((perf_counter() - provider_started) * 1000),
                ))

                if not self._should_fallback(exc):
                    await self._save(self._failed_record(
                        request, started_at, total_started, attempts, exc
                    ))
                    raise

        exc = AllProvidersFailedException(failures)
        await self._save(self._failed_record(
            request, started_at, total_started, attempts, exc
        ))
        raise exc

    async def _save(self, record: LlmCallRecord) -> None:
        """记录失败不能改变 LLM 调用结果。"""
        try:
            await self.recorder.save(record)
        except Exception:
            logger.warning("Failed to save LLM call record", exc_info=True)

    # 这些函数只映射 requestId、traceId、Provider、模型、usage、耗时和安全错误信息。
    # 不写入 Prompt、响应正文、请求头或 API Key。
    @staticmethod
    def _success_attempt(
        response: UnifiedChatResponse,
        started_at: datetime,
        latency_ms: int,
    ) -> ProviderAttemptRecord:
        """创建成功的 Provider 尝试记录。"""
        return ProviderAttemptRecord(
            provider=response.provider,
            model=response.model,
            started_at=started_at,
            ended_at=datetime.now(UTC),
            status="SUCCESS",
            retry_count=int(response.metadata.get("retryCount", 0)),
            provider_latency_ms=latency_ms,
        )

    @staticmethod
    def _failed_attempt(
        client: LlmProviderClient,
        error: LlmProviderException,
        started_at: datetime,
        latency_ms: int,
    ) -> ProviderAttemptRecord:
        """创建失败的 Provider 尝试记录。"""
        return ProviderAttemptRecord(
            provider=LlmProvider(client.provider),
            model="",
            started_at=started_at,
            ended_at=datetime.now(UTC),
            status="FAILED",
            retry_count=error.retry_count,
            provider_latency_ms=latency_ms,
            error_type=type(error).__name__,
            status_code=error.status_code,
        )

    @staticmethod
    def _success_record(
        request: UnifiedChatRequest,
        started_at: datetime,
        response: UnifiedChatResponse,
        attempts: list[ProviderAttemptRecord],
    ) -> LlmCallRecord:
        """创建成功的整次调用记录。"""
        return LlmCallRecord(
            request_id=request.metadata.get("requestId"),
            trace_id=request.metadata.get("traceId"),
            started_at=started_at,
            ended_at=datetime.now(UTC),
            status="SUCCESS",
            provider=response.provider,
            model=response.model,
            usage=response.usage,
            total_latency_ms=response.total_latency_ms or 0,
            fallback_path=[attempt.provider for attempt in attempts],
            attempts=list(attempts),
        )

    @staticmethod
    def _failed_record(
        request: UnifiedChatRequest,
        started_at: datetime,
        total_started: float,
        attempts: list[ProviderAttemptRecord],
        error: Exception,
    ) -> LlmCallRecord:
        """创建失败的整次调用记录。"""
        final_error = (
            error.failures[-1]
            if isinstance(error, AllProvidersFailedException) and error.failures
            else error
        )
        status_code = (
            final_error.status_code
            if isinstance(final_error, LlmProviderException)
            else -1
        )

        return LlmCallRecord(
            request_id=request.metadata.get("requestId"),
            trace_id=request.metadata.get("traceId"),
            started_at=started_at,
            ended_at=datetime.now(UTC),
            status="FAILED",
            provider=None,
            model=None,
            usage=TokenUsage(),
            total_latency_ms=int((perf_counter() - total_started) * 1000),
            fallback_path=[attempt.provider for attempt in attempts],
            attempts=list(attempts),
            final_error_type=type(final_error).__name__,
            final_status_code=status_code,
        )

    @staticmethod
    def _should_fallback(exc: LlmProviderException) -> bool:
        """只对限流、5xx、超时、网络错误降级。"""
        return exc.status_code in {429, 500, 502, 503, 504, -1}
```
