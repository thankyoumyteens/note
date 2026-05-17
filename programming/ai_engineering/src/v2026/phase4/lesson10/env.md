# 创建 .env

在 `python-tools/.env` 中写：

```env
OPENAI_API_KEY=你的-api-key
OPENAI_BASE_URL=https://api.openai.com
OPENAI_MODEL=gpt-4o-mini
```

如果你用 OpenAI-compatible 平台：

```env
OPENAI_API_KEY=你的兼容平台-key
OPENAI_BASE_URL=https://你的兼容平台域名
OPENAI_MODEL=你的模型名
```

注意：

```text
base-url 不要重复带 /v1，脚本里会拼 /v1/chat/completions。
```
