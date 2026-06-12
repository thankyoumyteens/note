# Agent 开发

Agent 开发就是：开发一个能调用大模型、理解任务、拆解步骤、使用工具、访问知识库、执行流程，并把结果交付给用户的 AI 应用系统。

它不是单纯“调用 ChatGPT API”，而是把大模型变成一个可以完成业务任务的“智能执行系统”。

普通 LLM 应用大概是：

```text
用户输入问题 → 调用大模型 → 返回答案
```

例如：

```text
用户：帮我总结这段文字
AI：这是总结……
```

Agent 开发是：

```text
用户提出任务
→ Agent 理解目标
→ 拆解步骤
→ 判断需要哪些工具
→ 调用数据库 / API / 搜索 / 文档库
→ 处理中间结果
→ 必要时继续调用工具
→ 最后返回结果
```

例如：

```text
用户：帮我查一下这个客户最近的订单，并生成一封催付款邮件
```

Agent 可能会做：

```text
1. 理解任务：查订单 + 写邮件
2. 调用订单系统 API
3. 查询客户欠款记录
4. 判断是否逾期
5. 生成邮件草稿
6. 返回给用户确认
```

这就是 Agent 开发。

## Agent 开发的典型技术栈

### Java 路线

需要掌握：

- Java 21
- Spring Boot
- Spring Cloud
- MyBatis / JPA
- PostgreSQL / MySQL
- Redis
- Kafka
- Spring AI
- LangChain4j
- pgvector / Milvus / Elasticsearch
- Docker / K8s

适合你这种 Java 后端背景。

### Python 路线

需要掌握：

- Python
- FastAPI
- LangChain
- LangGraph
- LlamaIndex
- AutoGen
- Dify
- Chroma / FAISS / Milvus
- PyTorch 基础

Python 在 Agent 原型、RAG、实验、AI 框架生态里更常见。

### 平台路线

需要掌握：

- Dify
- Coze
- n8n
- Flowise
- FastGPT
- LangGraph Platform
- MCP
- Claude Code / Codex / Cursor

适合快速做业务原型和企业内部工具。
