# application.yml 配置

API Key 不写在配置文件中，而是放到环境变量中。

```yaml
llm:
  default-provider: openai

  providers:
    openai:
      type: openai-compatible
      base-url: https://api.openai.com/v1
      api-key: ${OPENAI_API_KEY}
      model: gpt-5.4

    qwen:
      type: openai-compatible
      base-url: https://dashscope.aliyuncs.com/compatible-mode/v1
      api-key: ${DASHSCOPE_API_KEY}
      model: qwen3.7-plus

    deepseek:
      type: openai-compatible
      base-url: https://api.deepseek.com
      api-key: ${DEEPSEEK_API_KEY}
      model: deepseek-v4-pro

    claude:
      type: anthropic
      base-url: https://api.anthropic.com/v1
      api-key: ${ANTHROPIC_API_KEY}
      model: claude-sonnet-4-6
```

实际项目里，模型名要以各家控制台和官方模型列表为准。尤其是 DeepSeek 官方已经标注 `deepseek-chat` 和 `deepseek-reasoner` 会废弃，当前推荐 `deepseek-v4-flash` / `deepseek-v4-pro`。
