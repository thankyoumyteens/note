# 安装 Claude Code

```sh
npm install -g @anthropic-ai/claude-code
# 升级
npm update -g @anthropic-ai/claude-code
```

## 安装 Claude Code Router

```sh
npm install -g @musistudio/claude-code-router
# 升级
npm update -g @musistudio/claude-code-router
```

**创建 CCR 配置：**

```sh
mkdir ~/.claude-code-router/
vim ~/.claude-code-router/config.json
```

**配置大模型：**

```json
{
  // 您可以通过将其设置为 true 来启用日志记录
  "LOG": false,
  "LOG_LEVEL": "debug",
  "CLAUDE_PATH": "",
  // 设置中转服务的主机地址和端口
  "HOST": "127.0.0.1",
  "PORT": 3456,
  "APIKEY": "",
  "API_TIMEOUT_MS": "600000",
  // 您可以为 API 请求设置代理
  "PROXY_URL": "http://127.0.0.1:10808",
  "transformers": [],
  // 用于配置不同的模型提供商(数组, 可以配置多个厂商)
  "Providers": [
    {
      // 提供商的唯一名称
      "name": "EdenAI",
      // 聊天补全的完整 API 端点
      "api_base_url": "https://api.edenai.run/v3/llm/chat/completions",
      // 您提供商的 API 密钥
      "api_key": "xxx",
      // 此提供商可用的模型名称列表
      "models": ["openai/gpt-5.4"]
    }
  ],
  "StatusLine": {
    "enabled": false,
    "currentStyle": "default",
    "default": {
      "modules": []
    },
    "powerline": {
      "modules": []
    }
  },
  // 用于设置路由规则。default 指定默认模型，如果未配置其他路由，则该模型将用于所有请求
  "Router": {
    "default": "EdenAI,openai/gpt-5.4",
    "background": "EdenAI,openai/gpt-5.4",
    "think": "EdenAI,openai/gpt-5.4",
    "longContext": "EdenAI,openai/gpt-5.4",
    "longContextThreshold": 60000,
    "webSearch": "EdenAI,openai/gpt-5.4",
    "image": ""
  },
  "CUSTOM_ROUTER_PATH": ""
}
```

**修改配置文件后，需要重启服务使配置生效：**

```sh
ccr restart
```

**使用 router 启动 Claude Code：**

```sh
ccr code
```
