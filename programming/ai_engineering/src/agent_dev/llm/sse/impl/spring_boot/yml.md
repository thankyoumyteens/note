# application.yml

```yaml
app:
  ai:
    providers:
      deepseek:
        type: openai-chat-completions
        api-key: ${DEEPSEEK_API_KEY}
        base-url: https://api.deepseek.com
        path: /chat/completions
        model: deepseek-v4-pro
        temperature: 0.2
        max-tokens: 1000

      openai:
        type: openai-chat-completions
        api-key: ${OPENAI_API_KEY}
        base-url: https://api.openai.com/v1
        path: /chat/completions
        model: gpt-4o-mini
        temperature: 0.2
        max-tokens: 1000

      claude:
        type: anthropic-messages
        api-key: ${ANTHROPIC_API_KEY}
        base-url: https://api.anthropic.com/v1
        path: /messages
        model: claude-haiku-4-5
        temperature: 0.2
        max-tokens: 1000
```
