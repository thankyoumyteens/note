# 配置类

不要在代码里到处 `os.environ["xxx"]`。正式项目应该统一配置入口。

编辑 settings.py：

```python
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """LLM provider 配置。

    所有 API Key 都从环境变量或 .env 读取，避免写死在代码里。
    """

    model_config = SettingsConfigDict(
        # 读取项目根目录下的 .env 文件
        env_file=".env",
        env_file_encoding="utf-8",
        # .env 里如果有 Settings 类没有声明的字段，直接忽略，不报错
        extra="ignore",
    )

    openai_api_key: str
    anthropic_api_key: str
    dashscope_api_key: str
    deepseek_api_key: str

    openai_base_url: str = "https://api.openai.com/v1"
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    deepseek_base_url: str = "https://api.deepseek.com"

    openai_model: str = "gpt-4o-mini"
    qwen_model: str = "qwen3.7-plus"
    deepseek_model: str = "deepseek-v4-pro"
    claude_model: str = "claude-haiku-4-5"


# 它会真正创建配置对象，并触发读取配置
settings = Settings()
```
