# 阶段 1：模型 API 工程化

## 第 1 阶段项目：AI Gateway

**最终目标**

做一个 Java 后端服务，统一封装大模型调用能力：

```text
前端 / 业务系统
   ↓
AI Gateway
   ↓
OpenAI / Claude / Gemini / DeepSeek / Qwen 等模型
```

这个 AI Gateway 后面会继续扩展成：

```text
AI Gateway
  ├── 普通聊天
  ├── 流式输出
  ├── 结构化输出
  ├── Function Calling
  ├── RAG
  ├── Agent
  ├── MCP 工具调用
  └── 调用日志 / 成本统计 / 限流 / fallback
```
