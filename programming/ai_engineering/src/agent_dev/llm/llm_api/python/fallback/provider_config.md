# provider 配置

## .env

```
OPENAI_API_KEY=your_openai_key
DEEPSEEK_API_KEY=your_deepseek_key
ANTHROPIC_API_KEY=your_anthropic_key

OPENAI_BASE_URL=https://api.openai.com/v1
DEEPSEEK_BASE_URL=https://api.deepseek.com
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1

OPENAI_MODEL=gpt-4o-mini
DEEPSEEK_MODEL=deepseek-v4-pro
ANTHROPIC_MODEL=claude-haiku-4-5

LLM_PROVIDER_ORDER=openai,deepseek,anthropic
```

## settings.py

```py
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """统一读取 LLM provider 配置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str  # OpenAI API Key。
    deepseek_api_key: str  # DeepSeek API Key。
    anthropic_api_key: str  # Anthropic API Key。

    openai_base_url: str = "https://api.openai.com/v1"  # OpenAI Base URL。
    deepseek_base_url: str = "https://api.deepseek.com"  # DeepSeek Base URL。
    anthropic_base_url: str = "https://api.anthropic.com/v1"  # Anthropic Base URL。

    openai_model: str = "gpt-4o-mini"  # OpenAI 模型名。
    deepseek_model: str = "deepseek-v4-pro"  # DeepSeek 模型名。
    anthropic_model: str = "claude-haiku-4-5"  # Anthropic 模型名。

    llm_provider_order: str = "openai,deepseek,anthropic"  # provider 降级顺序。
    request_timeout_seconds: float = 35.0  # 单次请求超时时间。
    max_retries: int = 2  # 当前 provider 内部最大重试次数。

    @property
    def provider_order(self) -> list[str]:
        """把逗号分隔的 provider 顺序转成列表。"""
        return [item.strip() for item in self.llm_provider_order.split(",") if item.strip()]


settings = Settings()
```
