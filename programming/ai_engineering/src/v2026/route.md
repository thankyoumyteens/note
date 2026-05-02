# Java转AI应用开发(2026)

## 阶段 1：Java AI Gateway

目标：掌握大模型 API 工程化调用。

学习内容：

```text
Spring Boot
WebClient
OpenAI-compatible API
普通聊天
流式输出 SSE
结构化输出
错误处理
API Key 配置
超时设置
```

项目产出：

```text
ai-gateway
  ├── /api/ai/chat
  ├── /api/ai/chat/stream
  └── /api/ai/extract-task
```

---

## 阶段 2：结构化输出与 Function Calling

目标：让 AI 输出能被 Java 业务系统稳定消费。

学习内容：

```text
JSON Schema
DTO 映射
Jackson 解析
输出校验
JSON 修复
Function Calling
Tool Calling
工具参数校验
工具执行结果封装
```

项目产出：

```text
任务抽取接口
订单查询工具调用接口
简单 Agent 工具调用 Demo
```

---

## 阶段 3：AI Gateway 生产化

目标：把 Demo 服务升级成生产级服务。

学习内容：

```text
调用日志
Token 统计
成本统计
限流
重试
熔断
Fallback 模型
请求追踪
异常分类
Prompt 版本管理
```

项目产出：

```text
可观测 AI Gateway
支持多模型供应商
支持 fallback
支持调用审计
```

---

## 阶段 4：Python AI 工具补齐

目标：补齐 AI 生态主流工具能力，但不转主线。

学习内容：

```text
Python 基础
venv / uv
FastAPI
Pydantic
httpx
pandas
LlamaIndex
LangGraph 基础
RAGAS
文档解析
embedding 批处理
```

项目产出：

```text
Python 文档处理 Worker
Python RAG 评估脚本
Python embedding 批处理脚本
```

---

## 阶段 5：RAG 系统

目标：构建企业知识库问答系统。

学习内容：

```text
文档上传
PDF / Word / Excel 解析
Chunking
Embedding
向量数据库
Hybrid Search
Rerank
引用来源
无答案拒答
RAG 评估
```

推荐技术：

```text
Java Spring Boot：主服务
Python Worker：文档解析与评估
Qdrant / Milvus / pgvector：向量库
Elasticsearch / OpenSearch：关键词检索
```

项目产出：

```text
企业知识库 RAG 系统
支持上传文档
支持带引用回答
支持检索日志
```

---

## 阶段 6：权限隔离 RAG

目标：做出真正有企业价值的 RAG。

学习内容：

```text
多租户
RBAC
文档级权限
Chunk 级 metadata
检索前权限过滤
检索后二次校验
审计日志
越权防护
Prompt Injection 防御
```

项目产出：

```text
多租户权限隔离知识库
用户只能检索自己有权限的文档
答案必须带引用
```

---

## 阶段 7：Agent 工作流

目标：让 AI 能安全调用工具、执行任务。

学习内容：

```text
Tool Calling
状态机
LangGraph
Human-in-the-loop
任务恢复
工具超时
工具重试
工具权限
工具审计
```

项目产出：

```text
工单处理 Agent
邮件 / Jira / GitLab / 知识库多工具协作
高风险操作需要人工确认
```

---

## 阶段 8：MCP 企业集成

目标：把企业内部系统封装成 AI 可调用工具。

学习内容：

```text
MCP Client
MCP Server
Tools
Resources
Prompts
Spring AI MCP
OAuth
Tool allowlist
权限透传
审计日志
MCP 安全
```

项目产出：

```text
企业 MCP Gateway
封装订单系统、工单系统、知识库、数据库查询工具
```

---

## 阶段 9：Text-to-SQL / BI Copilot

目标：做高价值数据分析类 AI 应用。

学习内容：

```text
Schema 理解
语义层
SQL 生成
SQL AST 校验
只读查询
LIMIT 注入
慢查询防护
字段脱敏
查询审计
图表生成
```

项目产出：

```text
安全 BI Copilot
自然语言查询数据
生成 SQL 和图表
禁止危险 SQL
```

---

## 阶段 10：LLMOps 与综合项目

目标：具备上线、监控、评估、迭代能力。

学习内容：

```text
Tracing
Evals
RAG 评估
Agent 评估
成本监控
质量回归测试
Prompt 版本管理
模型路由
A/B 测试
安全测试
```

最终项目：

```text
企业 AI 助手平台
  ├── AI Gateway
  ├── 企业 RAG
  ├── 权限系统
  ├── MCP Gateway
  ├── Agent 工作流
  ├── Text-to-SQL
  └── LLMOps Dashboard
```

---

# 最终路线一句话

```text
Java 后端主线
  -> AI Gateway
  -> 结构化输出 / Function Calling
  -> Python 工具补齐
  -> RAG
  -> 权限隔离 RAG
  -> Agent
  -> MCP
  -> LLMOps
```

你的定位：

```text
Java 后端开发
升级为
企业级 AI 应用开发工程师
```

不是全面转 Python，而是：

```text
Java 做生产系统
Python 做 AI 工具和数据处理
```
