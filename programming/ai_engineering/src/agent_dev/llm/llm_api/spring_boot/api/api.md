# 如何调用模型 API

Spring Boot 里调用 OpenAI / Claude / Qwen / DeepSeek，本质上要掌握三件事：

1. 每家 API 的请求格式
2. 在 Spring Boot 里如何封装 HTTP Client
3. 如何把多家模型统一成一个 LLM Client
