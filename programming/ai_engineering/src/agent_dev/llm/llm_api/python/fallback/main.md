# main

main.py

```py
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from llm_api_demo.exceptions import AllProvidersFailedException, LlmProviderException
from llm_api_demo.fallback_router import ProviderFallbackRouter
from llm_api_demo.provider_clients import (
    AnthropicProviderClient,
    DeepSeekProviderClient,
    LlmProviderClient,
    OpenAiResponsesProviderClient,
)
from llm_api_demo.schemas import UnifiedChatRequest, UnifiedChatResponse
from llm_api_demo.settings import settings

app = FastAPI(title="LLM Fallback Demo")


def build_clients() -> list[LlmProviderClient]:
    """根据配置顺序装配 provider clients。"""
    client_map: dict[str, LlmProviderClient] = {
        "openai": OpenAiResponsesProviderClient(),
        "deepseek": DeepSeekProviderClient(),
        "anthropic": AnthropicProviderClient(),
    }

    return [client_map[name] for name in settings.provider_order]


router = ProviderFallbackRouter(build_clients())


@app.post("/api/ai/chat")
async def chat(request: UnifiedChatRequest) -> UnifiedChatResponse:
    """带重试和降级的异步聊天接口。"""
    try:
        return await router.chat(request)
    except LlmProviderException as exc:
        # 非临时错误或单个 provider 已经明确失败时，返回网关错误给前端。
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except AllProvidersFailedException as exc:
        # 所有 provider 都失败，说明降级链已经耗尽。
        raise HTTPException(status_code=503, detail=str(exc)) from exc
```

## 运行

```sh
uv run uvicorn llm_api_demo.main:app --reload --port 8000
```

## 测试

```sh
curl -X POST http://127.0.0.1:8000/api/ai/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "system": "You are a helpful assistant.",
    "messages": [
      {
        "role": "user",
        "content": "用一句话解释什么是 LLM fallback。"
      }
    ],
    "options": {
      "temperature": 0.2,
      "max_tokens": 1000
    },
    "metadata": {}
  }' | jq
```
