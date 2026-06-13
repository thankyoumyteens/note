# OpenAI：Responses API

OpenAI 新项目建议优先用 Responses API，而不是 Chat Completions。Responses 提供更强的 agentic primitives、内置工具和状态能力。

```python
class OpenAiResponsesClient:
    """OpenAI Responses API 客户端。

    适合 OpenAI 官方模型的新项目。
    """

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)

    def chat(self, message: str) -> LlmResult:
        try:
            response = self.client.responses.create(
                model=settings.openai_model,
                instructions="You are a helpful assistant.",
                input=message,
                temperature=0.2,
                max_output_tokens=1000,
                store=False,
            )
        except OpenAIAPIError as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        return LlmResult(
            provider=LlmProvider.OPENAI,
            model=settings.openai_model,
            content=response.output_text,
        )
```

注意这里加了：

```python
store=False
```

这是正式项目更稳的默认值。除非你明确需要 OpenAI 保存 response state，否则不要默认存储。
