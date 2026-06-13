# DeepSeek：OpenAI-compatible

DeepSeek 也用 `openai` SDK 调。

```python
class DeepSeekClient:
    """DeepSeek OpenAI-compatible 客户端。"""

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    def chat(self, message: str) -> LlmResult:
        try:
            response = self.client.chat.completions.create(
                model=settings.deepseek_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
                temperature=0.2,
                max_tokens=1000,
            )
        except OpenAIAPIError as exc:
            raise RuntimeError(f"DeepSeek request failed: {exc}") from exc

        content = response.choices[0].message.content or ""

        return LlmResult(
            provider=LlmProvider.DEEPSEEK,
            model=settings.deepseek_model,
            content=content,
        )
```
