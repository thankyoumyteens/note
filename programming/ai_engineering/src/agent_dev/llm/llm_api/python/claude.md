# Claude：Anthropic SDK

使用 Anthropic 原生 Messages API。

```python
class ClaudeClient:
    """Claude / Anthropic Messages API 客户端。"""

    def __init__(self) -> None:
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    def chat(self, message: str) -> LlmResult:
        try:
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=1000,
                temperature=0.2,
                system="You are a helpful assistant.",
                messages=[
                    {"role": "user", "content": message},
                ],
            )
        except AnthropicAPIError as exc:
            raise RuntimeError(f"Claude request failed: {exc}") from exc

        text_parts: list[str] = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)

        return LlmResult(
            provider=LlmProvider.CLAUDE,
            model=settings.claude_model,
            content="".join(text_parts),
        )
```
