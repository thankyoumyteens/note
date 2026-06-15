# settings.py

```python
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """应用配置。默认从项目根目录 .env 读取。"""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str
    deepseek_api_key: str
    anthropic_api_key: str

    openai_base_url: str = "https://api.openai.com/v1"
    deepseek_base_url: str = "https://api.deepseek.com"
    anthropic_base_url: str = "https://api.anthropic.com"

    openai_model: str = "gpt-4o-mini"
    deepseek_model: str = "deepseek-chat"
    claude_model: str = "claude-haiku-4-5"

    temperature: float = 0.2
    max_tokens: int = 1000


settings = Settings()
```
