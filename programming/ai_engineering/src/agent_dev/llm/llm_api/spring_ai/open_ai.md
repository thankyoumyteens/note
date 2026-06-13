# 调用 OpenAI

application.yml:

```yaml
spring:
  ai:
    model:
      chat: openai

    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: https://api.openai.com
      chat:
        completions-path: /v1/chat/completions
        options:
          model: gpt-4o-mini
          temperature: 0.2
          max-tokens: 1000
```

如果用的是官方 OpenAI，通常可以不写 base-url 和 completions-path，用默认值就行。Spring AI 的默认 base-url 是 OpenAI API 地址，Chat Completions 路径默认是 /v1/chat/completions。

启动前设置环境变量：

```bash
export OPENAI_API_KEY="你的 OpenAI API Key"
```

此时注入的 `ChatClient.Builder` 背后就是 OpenAI ChatModel。
