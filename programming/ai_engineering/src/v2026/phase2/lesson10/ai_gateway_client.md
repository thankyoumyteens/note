# 创建 AiGatewayClient

封装 Python 调用 Java AI Gateway 的 HTTP 请求。

不要让每个 Python 脚本都手写 URL、timeout、错误处理。和 Java 里抽象 `LlmClient` 类似，Python 侧也要有一个小 client。

HTTPX 官方文档说明它默认有 timeout，默认网络不活动 5 秒会超时；本课仍显式设置 timeout，避免脚本卡死。

#### 代码

文件：

```text
python-tools/src/ai_gateway_tools/client.py
```

代码：

```python
from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv

from ai_gateway_tools.models import (
    ChatResponse,
    OrderAssistantResponse,
    TaskExtractionResult,
)


class AiGatewayClient:
    """
    Java AI Gateway 的 Python 辅助客户端。

    这个类只用于脚本、eval、批处理和后续 RAG 工具。
    它不是主后端，不替代 Java 服务。
    """

    def __init__(self, base_url: str | None = None, timeout: float = 60.0) -> None:
        load_dotenv()

        self.base_url = (base_url or os.getenv("AI_GATEWAY_BASE_URL") or "http://localhost:8080").rstrip("/")
        self.timeout = timeout

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )

    def close(self) -> None:
        """关闭底层 HTTP client。"""
        self._client.close()

    def chat(self, message: str) -> ChatResponse:
        """
        调用 Java 接口：POST /api/ai/chat
        """
        if not message.strip():
            raise ValueError("message cannot be empty")

        response = self._client.post(
            "/api/ai/chat",
            json={"message": message},
        )
        response.raise_for_status()

        return ChatResponse.model_validate(response.json())

    def extract_task(self, text: str) -> TaskExtractionResult:
        """
        调用 Java 接口：POST /api/ai/extract-task
        """
        if not text.strip():
            raise ValueError("text cannot be empty")

        response = self._client.post(
            "/api/ai/extract-task",
            json={"text": text},
        )
        response.raise_for_status()

        return TaskExtractionResult.model_validate(response.json())

    def order_assistant(self, message: str) -> OrderAssistantResponse:
        """
        调用 Java 接口：POST /api/ai/order-assistant
        """
        if not message.strip():
            raise ValueError("message cannot be empty")

        response = self._client.post(
            "/api/ai/order-assistant",
            json={"message": message},
        )
        response.raise_for_status()

        return OrderAssistantResponse.model_validate(response.json())

    def __enter__(self) -> "AiGatewayClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
```

#### 代码说明

`model_validate(response.json())` 会让 Pydantic 校验 Java 返回结果。 `model_validate()` 用于校验给定对象，`model_validate_json()` 用于校验 JSON 数据。
