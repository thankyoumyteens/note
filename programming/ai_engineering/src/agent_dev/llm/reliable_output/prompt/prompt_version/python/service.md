# IntentClassificationService

intent_service.py

```py
from __future__ import annotations

import logging
from uuid import UUID

from llm_api_demo.fallback_router import ProviderFallbackRouter
from llm_api_demo.prompt_registry import PromptRegistry, PromptSelection
from llm_api_demo.prompt_template import PromptRenderer
from llm_api_demo.schemas import (
    LlmGenerationOptions,
    UnifiedChatMessage,
    UnifiedChatRequest,
    UnifiedChatResponse,
)


# 复用 Uvicorn 已配置的日志器，使 --log-level debug 对业务日志生效。
logger = logging.getLogger("uvicorn.error")


class IntentClassificationService:
    """解析当前 Prompt 版本，并异步调用统一 Provider Router。"""

    def __init__(
        self,
        renderer: PromptRenderer,
        registry: PromptRegistry,
        selection: PromptSelection,
        router: ProviderFallbackRouter,
    ) -> None:
        self.renderer = renderer  # 将模板变量渲染为最终消息。
        self.registry = registry  # 保存全部不可变 Prompt 版本。
        self.selection = selection  # 应用配置指定的当前版本。
        self.router = router  # 复用异步重试和 Provider 降级入口。

    async def classify(
        self,
        user_input: str,
        request_id: UUID,
        trace_id: UUID,
    ) -> UnifiedChatResponse:
        if not user_input or not user_input.strip():
            raise ValueError("user_input must not be blank")

        definition = self.registry.require(self.selection)
        prompt = self.renderer.render(
            definition.template,
            {"user_input": user_input},
        )

        messages = [*definition.examples]
        # 当前输入始终位于该版本的全部 Few-shot 示例之后。
        messages.append(UnifiedChatMessage.user(prompt.user))

        request = UnifiedChatRequest(
            system=prompt.system,
            messages=messages,
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

        logger.debug(
            "Rendered prompt: name=%s version=%s system=%s messages=%s",
            prompt.prompt_name,
            prompt.prompt_version,
            prompt.system,
            messages,
        )

        return await self.router.chat(request)
```

在前文 `main.py` 中替换 Prompt 配置 import 和 Service 创建：

```py
from llm_api_demo.prompts import (
    INTENT_CLASSIFIER_REGISTRY,
    INTENT_CLASSIFIER_SELECTION,
)

intent_service = IntentClassificationService(
    renderer=PromptRenderer(),
    registry=INTENT_CLASSIFIER_REGISTRY,
    selection=INTENT_CLASSIFIER_SELECTION,
    router=router,
)
```

这里复用前文调用记录使用的 `uvicorn.error` logger，因此 `--log-level debug` 可以同时控制 Uvicorn 和 Prompt 调试日志。本地调试时执行：

```sh
uv run uvicorn llm_api_demo.main:app --reload --port 8000 --log-level debug
```

FastAPI endpoint、异常处理和测试请求保持不变。网络调用仍由 `await self.router.chat(request)` 异步执行。日志包含用户输入，只应在受控调试环境开启。
