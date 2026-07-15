# 自定义异常

exceptions.py

```py
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LlmProviderException(Exception):
    """单个 provider 调用失败。"""

    provider: str  # 失败的 provider 名称。
    status_code: int  # HTTP 状态码；-1 表示网络、超时等本地异常。
    message: str  # 错误说明。
    response_body: str = ""  # provider 返回的原始错误内容。

    def __str__(self) -> str:
        return f"{self.provider} failed: status={self.status_code}, message={self.message}"


class AllProvidersFailedException(Exception):
    """所有 provider 都失败。"""

    def __init__(self, failures: list[LlmProviderException]) -> None:
        self.failures = list(failures)  # 按实际调用顺序保存失败原因。
        super().__init__("All LLM providers failed")
```
