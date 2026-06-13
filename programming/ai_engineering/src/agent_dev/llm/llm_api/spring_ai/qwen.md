# 调用 Qwen：走 OpenAI-compatible

Spring AI 没必要专门写一套 Qwen Client，可以使用 Spring AI OpenAI 接口，把 base-url、api-key、model 换成 DashScope / Model Studio 的配置。

## application.yml

```yaml
spring:
  ai:
    model:
      chat: openai

    openai:
      api-key: ${DASHSCOPE_API_KEY}
      base-url: https://dashscope.aliyuncs.com/compatible-mode
      chat:
        # 这行配置可以省略，默认就是 /v1/chat/completions
        completions-path: /v1/chat/completions
        options:
          model: qwen3.7-plus
          temperature: 0.2
          max-tokens: 1000
```

启动前设置：

```bash
export DASHSCOPE_API_KEY="你的 DashScope API Key"
```
