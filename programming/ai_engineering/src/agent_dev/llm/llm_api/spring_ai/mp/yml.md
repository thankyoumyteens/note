# application.yml

改成：

```yaml
app:
  ai:
    default-provider: qwen

    providers:
      openai:
        type: openai
        api-key: ${OPENAI_API_KEY}
        base-url: https://api.openai.com
        completions-path: /v1/chat/completions
        model: gpt-4o-mini
        temperature: 0.2
        max-tokens: 1000

      qwen:
        type: openai-compatible
        api-key: ${DASHSCOPE_API_KEY}
        base-url: https://dashscope.aliyuncs.com/compatible-mode
        completions-path: /v1/chat/completions
        model: qwen3.7-plus
        temperature: 0.2
        max-tokens: 1000

      claude:
        type: anthropic
        api-key: ${ANTHROPIC_API_KEY}
        base-url: https://api.anthropic.com
        completions-path: /v1/messages
        version: 2023-06-01
        model: claude-haiku-4-5
        temperature: 0.2
        max-tokens: 4096
```
