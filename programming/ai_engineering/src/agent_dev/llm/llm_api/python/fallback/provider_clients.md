# ProviderClient

provider_clients.py

```py
from __future__ import annotations

from abc import ABC, abstractmethod
from contextvars import ContextVar

from anthropic import AsyncAnthropic, APIError as AnthropicAPIError
from openai import APIConnectionError, APIError, APITimeoutError, AsyncOpenAI
from tenacity import RetryCallState, retry, retry_if_exception, stop_after_attempt, wait_random_exponential

from llm_api_demo.exceptions import LlmProviderException
from llm_api_demo.schemas import (
    ChatRole,
    LlmProvider,
    TokenUsage,
    UnifiedChatRequest,
    UnifiedChatResponse,
    UnifiedStopReason,
)
from llm_api_demo.settings import settings

retry_count_context: ContextVar[int] = ContextVar("retry_count", default=0)


def to_unified_stop_reason(reason: str | None) -> UnifiedStopReason | None:
    """将 Provider 原始停止原因映射为统一值。"""
    if reason is None:
        return None

    mapping = {
        "stop": UnifiedStopReason.STOP,
        "end_turn": UnifiedStopReason.STOP,
        "stop_sequence": UnifiedStopReason.STOP,
        "completed": UnifiedStopReason.STOP,
        "length": UnifiedStopReason.LENGTH,
        "max_tokens": UnifiedStopReason.LENGTH,
        "max_output_tokens": UnifiedStopReason.LENGTH,
        "tool_calls": UnifiedStopReason.TOOL_CALLS,
        "tool_use": UnifiedStopReason.TOOL_CALLS,
        "content_filter": UnifiedStopReason.CONTENT_FILTER,
        "refusal": UnifiedStopReason.CONTENT_FILTER,
    }
    return mapping.get(reason, UnifiedStopReason.OTHER)


class LlmProviderClient(ABC):
    """统一 ProviderClient 接口。

    这个接口对应 Spring Boot 版本里的 LlmProviderClient。
    上层 fallback router 只依赖这个抽象，不关心底层 provider 用的是
    OpenAI Responses API、OpenAI-compatible Chat Completions，还是
    Anthropic Messages API。
    """

    @property
    @abstractmethod
    def provider(self) -> str:
        """返回 provider 名称，用于记录失败链路和构造统一异常。"""

    @abstractmethod
    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        """异步发起统一聊天请求，并返回统一响应对象。"""


def should_retry_exception(exc: BaseException) -> bool:
    """判断当前异常是否允许在同一个 provider 内部重试。

    这里的规则和 Spring Boot 版本保持一致：
    - 429：限流或额度临时不足，可以等一等再试。
    - 5xx：provider 服务端或网关临时异常，可以重试。
    - -1：没有 HTTP status，通常是本地超时、连接失败、DNS 等网络问题。

    400 / 401 / 403 这类错误通常表示参数、认证或权限问题，
    重试没有意义，也不应该自动切换 provider 掩盖真实问题。
    """
    if isinstance(exc, LlmProviderException):
        return exc.status_code in {429, 500, 502, 503, 504, -1}

    return False


def record_retry_count(retry_state: RetryCallState) -> None:
    """把首次调用之后的实际重试次数写入最终异常。"""
    if retry_state.outcome is None or not retry_state.outcome.failed:
        return

    error = retry_state.outcome.exception()
    if isinstance(error, LlmProviderException):
        error.retry_count = retry_state.attempt_number - 1


def set_retry_count(retry_state: RetryCallState) -> None:
    """记录当前异步任务已经发生的重试次数。"""
    retry_count_context.set(retry_state.attempt_number - 1)


class OpenAiResponsesProviderClient(LlmProviderClient):
    """OpenAI Responses API ProviderClient。

    OpenAI 官方模型的新项目优先使用 Responses API。
    这个 client 负责把统一请求 UnifiedChatRequest 转成 Responses API
    需要的 instructions / input / max_output_tokens 等参数。
    """

    def __init__(self) -> None:
        # OpenAI SDK 会读取这里传入的 api_key、base_url 和 timeout。
        # timeout 对应 Spring Boot WebClient 里的 request timeout。
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            timeout=settings.request_timeout_seconds,
        )

    @property
    def provider(self) -> str:
        # provider 名称必须和 settings.provider_order 里的 openai 保持一致。
        return LlmProvider.OPENAI.value

    @retry(
        # 只重试 LlmProviderException 中被判断为临时性故障的异常。
        retry=retry_if_exception(should_retry_exception),
        # max_retries 表示失败后额外重试几次，所以总尝试次数要 + 1。
        stop=stop_after_attempt(settings.max_retries + 1),
        # 指数退避可以避免在 provider 限流或短暂抖动时立刻打满请求。
        wait=wait_random_exponential(multiplier=0.5, max=3),
        before=set_retry_count,
        after=record_retry_count,
        # 最后一次仍失败时，直接抛出原异常交给 fallback router 判断是否切 provider。
        reraise=True,
    )
    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        try:
            # Responses API 的 input 可以直接接收字符串。
            # 这里把多轮 user / assistant 消息压成文本，保持示例聚焦 fallback 主线。
            # 如果需要完整多轮结构，可以把 input 改成 Responses API 支持的 message 数组。
            user_text = "\n".join(message.content for message in request.messages)

            response = await self.client.responses.create(
                model=settings.openai_model,
                instructions=request.system,
                input=user_text,
                temperature=request.options.temperature,
                max_output_tokens=request.options.max_tokens,
                # 默认不让 OpenAI 保存 response state，正式项目里更稳妥。
                store=False,
            )

            # 把 OpenAI Responses API 的返回结果映射成统一响应对象，
            # 这样 router 和上层业务不需要感知 provider 的原始返回结构。
            return UnifiedChatResponse(
                provider=LlmProvider.OPENAI,
                model=response.model or settings.openai_model,
                content=response.output_text,
                stop_reason=to_unified_stop_reason(response.status),
                usage=TokenUsage(
                    input_tokens=response.usage.input_tokens if response.usage else None,
                    output_tokens=response.usage.output_tokens if response.usage else None,
                    total_tokens=response.usage.total_tokens if response.usage else None,
                ),
                metadata={
                    "response_id": response.id,
                    "raw_stop_reason": response.status,
                    "retry_count": retry_count_context.get(),
                },
            )
        except (APITimeoutError, APIConnectionError) as exc:
            # 超时、连接失败这类错误没有稳定的 HTTP 状态码，用 -1 表示本地调用失败。
            raise LlmProviderException(self.provider, -1, "OpenAI timeout or connection error") from exc
        except APIError as exc:
            # OpenAI SDK 的 APIError 通常带 status_code。
            # 这里统一包装成 LlmProviderException，方便重试和降级逻辑复用同一套判断。
            raise LlmProviderException(
                self.provider,
                getattr(exc, "status_code", -1) or -1,
                str(exc),
                str(getattr(exc, "response", "")),
            ) from exc


class DeepSeekProviderClient(LlmProviderClient):
    """DeepSeek OpenAI-compatible ProviderClient。

    DeepSeek 兼容 OpenAI Chat Completions 协议，所以仍然使用 openai SDK，
    但 base_url、api_key 和 model 都来自 DeepSeek 的配置。
    """

    def __init__(self) -> None:
        # 通过 base_url 切到 DeepSeek 服务端，其余调用方式仍沿用 OpenAI SDK。
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            timeout=settings.request_timeout_seconds,
        )

    @property
    def provider(self) -> str:
        # provider 名称用于降级链日志和异常信息。
        return LlmProvider.DEEPSEEK.value

    @retry(
        # DeepSeek 的 429 / 5xx / timeout 会先在当前 provider 内部重试。
        retry=retry_if_exception(should_retry_exception),
        stop=stop_after_attempt(settings.max_retries + 1),
        wait=wait_random_exponential(multiplier=0.5, max=3),
        before=set_retry_count,
        after=record_retry_count,
        reraise=True,
    )
    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        try:
            # Chat Completions 把 system 放在 messages 的第一条。
            messages = [{"role": "system", "content": request.system}]

            # 统一 DTO 中只保留 user / assistant 消息，这里直接转换成 OpenAI-compatible 格式。
            for message in request.messages:
                messages.append({"role": message.role.value, "content": message.content})

            response = await self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=messages,
                temperature=request.options.temperature,
                max_tokens=request.options.max_tokens,
                top_p=request.options.top_p,
            )

            # choices[0].message.content 是 Chat Completions 的主文本结果。
            content = response.choices[0].message.content or ""
            # usage 可能为空，所以映射 token 用量时要做空值判断。
            usage = response.usage

            return UnifiedChatResponse(
                provider=LlmProvider.DEEPSEEK,
                model=response.model or settings.deepseek_model,
                content=content,
                stop_reason=to_unified_stop_reason(response.choices[0].finish_reason),
                usage=TokenUsage(
                    input_tokens=usage.prompt_tokens if usage else None,
                    output_tokens=usage.completion_tokens if usage else None,
                    total_tokens=usage.total_tokens if usage else None,
                ),
                metadata={
                    "raw_stop_reason": response.choices[0].finish_reason,
                    "retry_count": retry_count_context.get(),
                },
            )
        except (APITimeoutError, APIConnectionError) as exc:
            # 本地网络或超时错误统一用 -1，后续 router 会把它视为可降级错误。
            raise LlmProviderException(self.provider, -1, "DeepSeek timeout or connection error") from exc
        except APIError as exc:
            # 统一保留 status_code 和 response body，方便排查 provider 原始失败原因。
            raise LlmProviderException(
                self.provider,
                getattr(exc, "status_code", -1) or -1,
                str(exc),
                str(getattr(exc, "response", "")),
            ) from exc


class AnthropicProviderClient(LlmProviderClient):
    """Anthropic Messages API ProviderClient。

    Anthropic 不使用 OpenAI-compatible Chat Completions 格式。
    它的 system 是单独参数，messages 里只放 user / assistant，
    所以这里单独做一次请求格式转换。
    """

    def __init__(self) -> None:
        # Anthropic SDK 只需要 api_key 和 timeout；base_url 保持 SDK 默认即可。
        self.client = AsyncAnthropic(
            api_key=settings.anthropic_api_key,
            timeout=settings.request_timeout_seconds,
        )

    @property
    def provider(self) -> str:
        # provider 名称必须和统一枚举、配置顺序保持一致。
        return LlmProvider.ANTHROPIC.value

    @retry(
        # Anthropic 临时错误也复用同一套重试判断。
        retry=retry_if_exception(should_retry_exception),
        stop=stop_after_attempt(settings.max_retries + 1),
        wait=wait_random_exponential(multiplier=0.5, max=3),
        before=set_retry_count,
        after=record_retry_count,
        reraise=True,
    )
    async def chat(self, request: UnifiedChatRequest) -> UnifiedChatResponse:
        try:
            # Anthropic Messages API 不允许把 system 混在 messages 里，
            # 所以这里过滤出 user / assistant 后，system 通过独立参数传入。
            messages = [
                {"role": message.role.value, "content": message.content}
                for message in request.messages
                if message.role in {ChatRole.USER, ChatRole.ASSISTANT}
            ]

            response = await self.client.messages.create(
                model=settings.anthropic_model,
                system=request.system,
                messages=messages,
                temperature=request.options.temperature,
                max_tokens=request.options.max_tokens,
            )

            # Anthropic 的 content 是 block 列表，文本内容需要从 type == "text" 的 block 中取出。
            text_parts = [
                block.text
                for block in response.content
                if block.type == "text"
            ]

            return UnifiedChatResponse(
                provider=LlmProvider.ANTHROPIC,
                model=response.model or settings.anthropic_model,
                content="".join(text_parts),
                stop_reason=to_unified_stop_reason(response.stop_reason),
                usage=TokenUsage(
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                ),
                metadata={
                    "raw_stop_reason": response.stop_reason,
                    "retry_count": retry_count_context.get(),
                },
            )
        except AnthropicAPIError as exc:
            # HTTP 异常保留原状态码；超时和网络错误没有状态码，统一使用 -1。
            status_code = getattr(exc, "status_code", -1) or -1
            raise LlmProviderException(
                self.provider,
                status_code,
                str(exc),
                str(getattr(exc, "response", "")),
            ) from exc
```
