# 配置 application.yml

在 `src/main/resources/application.yml` 加：

```yaml
server:
  port: 8080

llm:
  openai-compatible:
    base-url: https://api.openai.com
    api-key: ${OPENAI_API_KEY}
    model: gpt-5.1-mini
    timeout-seconds: 60
```

说明：

```text
base-url：模型 API 地址
api-key：从环境变量读取，不要写死在代码里
model：模型名称
timeout-seconds：请求超时时间
```

如果你用的是其他兼容 OpenAI 格式的平台，比如 DeepSeek、Qwen、Moonshot 等，只要改：

```yaml
base-url: 你的供应商地址
api-key: 你的 API Key
model: 你的模型名
```

注意：不同供应商的 `/v1/chat/completions` 兼容程度可能不同。
