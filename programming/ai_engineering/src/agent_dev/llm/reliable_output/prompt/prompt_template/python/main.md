# FastAPI 使用方式

基于前文的 `main.py`，增加下面的 import：

```py
from uuid import uuid4

from pydantic import BaseModel, Field

from llm_api_demo.intent_service import IntentClassificationService
from llm_api_demo.prompt_template import PromptRenderer
from llm_api_demo.prompts import INTENT_CLASSIFIER_PROMPT
```

在现有 `router` 创建完成后，创建 Service 并增加接口：

```py
intent_service = IntentClassificationService(
    renderer=PromptRenderer(),
    prompt_template=INTENT_CLASSIFIER_PROMPT,
    router=router,
)


class IntentClassificationRequest(BaseModel):
    """意图识别 HTTP 请求。"""

    user_input: str = Field(min_length=1)  # 需要识别意图的原始用户输入。


@app.post("/api/intents/classify")
async def classify_intent(
    request: IntentClassificationRequest,
) -> UnifiedChatResponse:
    """异步渲染 Prompt 并调用 Provider 降级链。"""
    request_id = uuid4()
    trace_id = request_id

    try:
        return await intent_service.classify(
            user_input=request.user_input,
            request_id=request_id,
            trace_id=trace_id,
        )
    except LlmProviderException as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except AllProvidersFailedException as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
```

这里复用前文 `main.py` 已导入的 `HTTPException`、`LlmProviderException`、`AllProvidersFailedException` 和 `UnifiedChatResponse`。

## 运行

```sh
uv run uvicorn llm_api_demo.main:app --reload --port 8000
```

## 测试接口

```sh
curl -sS -X POST "http://127.0.0.1:8000/api/intents/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "帮我查询订单 20260717001"
  }' | jq
```
