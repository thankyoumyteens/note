# main

main.py

```py
from __future__ import annotations

from llm_api_demo.provider_clients import (
    AnthropicProviderClient,
    DeepSeekProviderClient,
    LlmProviderClient,
    OpenAiResponsesProviderClient,
)
from llm_api_demo.fallback_router import ProviderFallbackRouter
from llm_api_demo.schemas import UnifiedChatMessage, UnifiedChatRequest
from llm_api_demo.settings import settings


def build_clients() -> list[LlmProviderClient]:
    """根据配置顺序装配 provider clients。"""
    client_map: dict[str, LlmProviderClient] = {
        "openai": OpenAiResponsesProviderClient(),
        "deepseek": DeepSeekProviderClient(),
        "anthropic": AnthropicProviderClient(),
    }

    return [client_map[name] for name in settings.provider_order]


def main() -> None:
    """演示一次带降级链的 LLM 调用。"""
    router = ProviderFallbackRouter(build_clients())

    request = UnifiedChatRequest(
        system="You are a helpful assistant.",
        messages=[
            UnifiedChatMessage.user("用一句话解释什么是 LLM fallback。"),
        ],
    )

    response = router.chat(request)

    print(f"provider: {response.provider}")
    print(f"model: {response.model}")
    print(response.content)


if __name__ == "__main__":
    main()
```

## 运行

```sh
uv run python -m llm_api_demo.main
```
