# IntentClassificationService

intent_service.py

```py
from __future__ import annotations

from uuid import UUID

from llm_api_demo.fallback_router import ProviderFallbackRouter
from llm_api_demo.prompt_template import PromptRenderer, PromptTemplate
from llm_api_demo.schemas import (
    LlmGenerationOptions,
    UnifiedChatMessage,
    UnifiedChatRequest,
    UnifiedChatResponse,
)


class IntentClassificationService:
    """渲染意图识别 Prompt，并异步调用统一 Provider Router。"""

    def __init__(
        self,
        renderer: PromptRenderer,
        prompt_template: PromptTemplate,
        router: ProviderFallbackRouter,
    ) -> None:
        self.renderer = renderer  # 将模板变量渲染为最终消息。
        self.prompt_template = prompt_template  # 意图识别模板及其版本。
        self.router = router  # 复用异步重试和 Provider 降级入口。

    async def classify(
        self,
        user_input: str,
        request_id: UUID,
        trace_id: UUID,
    ) -> UnifiedChatResponse:
        if not user_input or not user_input.strip():
            raise ValueError("user_input must not be blank")

        prompt = self.renderer.render(
            self.prompt_template,
            {"user_input": user_input},
        )

        request = UnifiedChatRequest(
            system=prompt.system,
            messages=[UnifiedChatMessage.user(prompt.user)],
            options=LlmGenerationOptions(
                temperature=0.0,
                max_tokens=300,
            ),
            metadata={
                "requestId": str(request_id),
                "traceId": str(trace_id),
                "promptName": prompt.prompt_name,
                "promptVersion": prompt.prompt_version,
            },
        )

        return await self.router.chat(request)
```

模板渲染是纯内存操作，不需要 `async def`。`classify()` 会等待异步 Router 完成网络调用，因此必须使用 `async def` 和 `await`。
