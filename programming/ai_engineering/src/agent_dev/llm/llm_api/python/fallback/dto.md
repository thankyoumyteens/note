# 统一 DTO

schemas.py

```py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class LlmProvider(StrEnum):
    """支持的模型服务商。"""

    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"


class ChatRole(StrEnum):
    """统一聊天角色。"""

    USER = "user"
    ASSISTANT = "assistant"


class UnifiedStopReason(StrEnum):
    """统一停止原因。"""

    STOP = "stop"
    LENGTH = "length"
    TOOL_CALLS = "tool_calls"
    CONTENT_FILTER = "content_filter"
    OTHER = "other"


@dataclass(frozen=True)
class UnifiedChatMessage:
    """统一消息结构。"""

    role: ChatRole  # 消息角色，只放 user / assistant。
    content: str  # 消息文本内容。

    def __post_init__(self) -> None:
        if not isinstance(self.role, ChatRole):
            raise ValueError("role must be a ChatRole")
        if not self.content or not self.content.strip():
            raise ValueError("content must not be blank")

    @staticmethod
    def user(content: str) -> "UnifiedChatMessage":
        """创建用户消息。"""
        return UnifiedChatMessage(role=ChatRole.USER, content=content)

    @staticmethod
    def assistant(content: str) -> "UnifiedChatMessage":
        """创建助手消息。"""
        return UnifiedChatMessage(role=ChatRole.ASSISTANT, content=content)


@dataclass(frozen=True)
class LlmGenerationOptions:
    """统一生成参数。"""

    temperature: float = 0.2  # 控制输出随机性。
    max_tokens: int = 1000  # 限制最大输出 token 数。
    top_p: float | None = None  # nucleus sampling 参数。


@dataclass(frozen=True)
class UnifiedChatRequest:
    """统一聊天请求。"""

    system: str  # 系统指令。
    messages: list[UnifiedChatMessage]  # 对话消息列表。
    options: LlmGenerationOptions = field(default_factory=LlmGenerationOptions)  # 生成参数。
    metadata: dict[str, Any] = field(default_factory=dict)  # 扩展元数据。

    def __post_init__(self) -> None:
        if not self.messages:
            raise ValueError("messages must not be empty")
        object.__setattr__(self, "system", self.system or "")
        object.__setattr__(self, "messages", list(self.messages))
        object.__setattr__(self, "options", self.options or LlmGenerationOptions())
        object.__setattr__(self, "metadata", dict(self.metadata or {}))


@dataclass(frozen=True)
class TokenUsage:
    """统一 token 用量。"""

    input_tokens: int | None = None  # 输入 token 数。
    output_tokens: int | None = None  # 输出 token 数。
    total_tokens: int | None = None  # 总 token 数。


@dataclass(frozen=True)
class UnifiedChatResponse:
    """统一聊天响应。"""

    provider: LlmProvider  # 实际命中的 provider。
    model: str  # 实际使用的模型。
    content: str  # 模型返回文本。
    stop_reason: UnifiedStopReason | None = None  # 统一停止原因；provider 未返回时为空。
    usage: TokenUsage = field(default_factory=TokenUsage)  # token 用量。
    provider_latency_ms: int | None = None  # 最终成功 ProviderClient 的完整耗时。
    total_latency_ms: int | None = None  # 整个 Router 调用耗时。
    metadata: dict[str, Any] = field(default_factory=dict)  # 扩展响应信息。

    def __post_init__(self) -> None:
        if not isinstance(self.provider, LlmProvider):
            raise ValueError("provider must be an LlmProvider")
        if not self.model or not self.model.strip():
            raise ValueError("model must not be blank")
        object.__setattr__(self, "content", self.content or "")
        object.__setattr__(self, "usage", self.usage or TokenUsage())
        object.__setattr__(self, "metadata", dict(self.metadata or {}))
```
