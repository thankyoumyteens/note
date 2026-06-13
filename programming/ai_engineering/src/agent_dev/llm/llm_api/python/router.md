# 统一 Router

```py
class LlmRouter:
    """统一 LLM 路由器。

    上层业务只传 provider，不直接依赖具体 SDK。
    """

    def __init__(self) -> None:
        self.openai = OpenAiResponsesClient()
        self.deepseek = DeepSeekClient()
        self.claude = ClaudeClient()

    def chat(self, provider: LlmProvider, message: str) -> LlmResult:
        match provider:
            case LlmProvider.OPENAI:
                return self.openai.chat(message)
            case LlmProvider.DEEPSEEK:
                return self.deepseek.chat(message)
            case LlmProvider.CLAUDE:
                return self.claude.chat(message)
```
