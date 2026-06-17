# application.yml

```yaml
app:
  ai:
    providers:
      openai:
        type: openai
        api-key: ${OPENAI_API_KEY}
        base-url: https://api.openai.com
        completions-path: /v1/chat/completions
        model: gpt-4o-mini
        temperature: 0.2
        max-tokens: 1000

      deepseek:
        type: openai-compatible
        api-key: ${DEEPSEEK_API_KEY}
        base-url: https://api.deepseek.com
        completions-path: /chat/completions
        model: deepseek-chat
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
        max-tokens: 1000
```
