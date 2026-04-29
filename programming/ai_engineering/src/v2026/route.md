# Java转AI应用开发(2026)

下面是一份**面向 2026 年的 Java 后端开发转型 AI 应用开发学习路线**。核心定位是：

> **不是从 Java 转去做 Python 算法工程师，而是把 Java 后端能力升级为“AI 应用工程能力”：模型 API、RAG、Agent、MCP、权限、安全、评估、上线运维。**

---

## 总体技术栈建议

### 主语言定位

| 方向                     | 推荐                                         |
| ------------------------ | -------------------------------------------- |
| 企业后端服务             | **Java / Spring Boot / Spring AI**           |
| AI 原型验证              | Python                                       |
| 文档解析、离线处理、评估 | Python 优先                                  |
| RAG 服务化               | Java 或 Python 都可                          |
| Agent 编排               | LangGraph / LlamaIndex Workflows / Spring AI |
| 企业系统集成             | Java 优先                                    |
| MCP Server               | Java/Spring 或 Python                        |
| 前端 Demo                | React / Next.js                              |
| 部署                     | Docker / Kubernetes / 云服务                 |

你不需要“放弃 Java”。
2026 年最合理的路线是：**Java 做生产服务，Python 做实验和数据处理。**

Spring AI 的目标就是把 Spring 生态中的可移植、模块化和 POJO 思维带到 AI 应用开发中；它的 `ChatClient` 支持同步和流式调用，也提供结构化输出能力。([Home][1])

---

# 阶段 0：补齐 AI 应用开发基础认知

## 目标

先建立正确认知：AI 应用开发不是“会写 Prompt”，而是**把不稳定的模型能力变成稳定的软件系统能力**。

## 你需要理解的核心变化

### 1. 从确定性系统到概率性系统

传统后端：

```text
输入 A -> 代码逻辑 -> 输出 B
```

AI 应用：

```text
输入 A + 上下文 + Prompt + 模型状态 -> 可能输出 B / B' / B''
```

所以你要学会：

- 输出校验
- 结构化输出
- 重试
- fallback
- 人工确认
- 日志追踪
- 成本控制
- 安全边界

### 2. 从 CRUD 到 AI Workflow

以前主要做：

```text
Controller -> Service -> DAO -> DB
```

AI 应用更像：

```text
用户请求
 -> 权限校验
 -> 意图识别
 -> 检索上下文
 -> 调用模型
 -> 工具调用
 -> 输出校验
 -> 审计记录
 -> 返回结果
```

### 3. 从“调用模型”到“构建 AI 系统”

你最终要掌握的是：

- 模型 API
- RAG
- Agent
- MCP
- 工具调用
- 结构化输出
- 多租户权限
- LLMOps
- 安全与评估

## 阶段产出

你应该能清楚回答：

- RAG 是什么，解决什么问题？
- Agent 和普通 Chatbot 有什么区别？
- Function Calling 和 MCP 有什么区别？
- 为什么 AI 应用必须做 eval？
- 为什么不能把模型输出直接信任？

---

# 阶段 1：模型 API 工程化

## 目标

掌握大模型 API 的生产级调用方式，而不是只会写一个 Demo。

## 核心内容

### 1. 主流模型 API

建议至少熟悉：

- OpenAI
- Anthropic Claude
- Google Gemini
- DeepSeek
- 阿里 Qwen
- 火山 / 智谱 / 月之暗面等国内模型平台

重点不是每个都深入，而是理解它们共同的抽象：

```text
messages / input
model
temperature
max tokens
streaming
tool calling
structured output
system instruction
context window
```

### 2. Responses API / Chat API

2026 年做新项目时，应该优先理解较新的 agentic API 形态。OpenAI 官方文档建议新项目使用 Responses API，并把 structured outputs、function calling、native tools 等作为核心能力。([OpenAI开发者][2])

你需要掌握：

- 普通对话调用
- 流式输出 streaming
- JSON Schema 结构化输出
- tool calling
- 多轮上下文管理
- 文件输入
- 图像输入
- 模型选择
- 错误处理

### 3. 结构化输出

这是 AI 应用开发的第一核心技能。

不要再依赖：

```text
“请严格输出 JSON，不要输出其他内容”
```

应该使用：

- JSON Schema
- Structured Outputs
- Function Calling
- Java DTO 映射
- Pydantic 校验
- 输出失败后的 retry / repair

OpenAI 官方明确区分：连接模型到工具、函数和数据时使用 function calling；需要模型按固定格式响应时使用 structured response format。([OpenAI开发者][3])

### 4. Java 侧实现

你需要掌握：

- Spring AI ChatClient
- Spring AI structured output
- Spring Boot 封装 AI Gateway
- WebFlux / SSE 做流式输出
- Resilience4j 做重试、熔断、限流
- Micrometer / OpenTelemetry 做监控

### 5. Python 侧实现

Python 不作为你的主后端，但要能写：

- API 原型
- Prompt 测试脚本
- 批量评估脚本
- 文档处理 pipeline
- notebook 实验

建议熟悉：

- OpenAI Python SDK
- Anthropic SDK
- FastAPI
- Pydantic
- pandas
- asyncio

## 阶段项目

做一个 **AI Gateway 服务**：

功能包括：

- 支持多个模型供应商
- 支持 streaming
- 支持 JSON Schema 输出
- 支持 tool calling
- 支持请求日志
- 支持 token 统计
- 支持失败重试和 fallback
- 暴露统一 REST API

## 阶段验收标准

你应该能做到：

- 模型返回格式不对时自动处理
- 模型超时后降级
- 流式输出到前端
- 每次调用都有成本、耗时、模型、输入输出记录
- Java 服务中能把模型输出映射为强类型 DTO

---

# 阶段 2：Prompt Engineering 升级为 Context Engineering

## 目标

不要停留在“提示词技巧”，而是学会设计模型可控输入环境。

## 需要学习的内容

### 1. 基础 Prompt 能力

仍然需要掌握：

- role instruction
- few-shot
- task decomposition
- format instruction
- constraint instruction
- negative examples
- prompt template

但它们只是基础。

### 2. 不建议再把 CoT 当核心

2026 年生产应用不应该依赖“让模型输出完整思维链”。更好的做法是：

- 让模型输出结论和可验证依据
- 使用结构化中间结果
- 用 evaluator 检查输出
- 用工具完成确定性计算
- 不向用户暴露内部推理过程

### 3. Context Engineering

真正重要的是：

- 给模型什么上下文
- 不给模型什么上下文
- 上下文顺序如何组织
- 如何压缩历史对话
- 如何插入检索结果
- 如何处理冲突信息
- 如何让模型引用来源
- 如何防止 Prompt Injection

### 4. Instruction Hierarchy

你要明确不同层级指令的优先级：

```text
系统规则 > 开发者规则 > 工具约束 > 用户输入 > 检索内容
```

RAG 和 Agent 场景里尤其重要，因为外部文档和工具返回结果都可能包含恶意指令。

## 阶段项目

做一个 **结构化信息抽取服务**：

输入：

- 邮件
- 合同片段
- 工单
- 简历
- 发票文本

输出：

- 固定 JSON Schema
- 置信度
- 缺失字段
- 需要人工确认的字段

## 阶段验收标准

你应该能做到：

- 不靠正则解析模型文本
- 输出可被 Java DTO 接收
- 错误字段能自动重试或标记
- 对注入式输入有基本防御

---

# 阶段 3：RAG 与企业知识库工程

## 目标

掌握企业级 RAG，而不是只会“文档切块 + 向量库 + 问答”。

## RAG 标准架构

```text
文档上传
 -> 文档解析
 -> 清洗
 -> 分块
 -> 元数据写入
 -> embedding
 -> 向量库 / 搜索引擎
 -> query rewrite
 -> hybrid retrieval
 -> rerank
 -> 权限过滤
 -> context assembly
 -> LLM answer
 -> citation
 -> eval
```

---

## 3.1 文档解析与知识入库

这是很多人忽视，但企业落地最难的部分。

你要学：

- PDF 解析
- Word / Excel / PPT 解析
- HTML / Markdown 解析
- 图片 OCR
- 表格抽取
- 图表理解
- 文档结构识别
- 标题层级保留
- 页码和来源定位
- 增量更新
- 去重
- 版本管理

建议工具：

- Unstructured
- LlamaParse
- PyMuPDF
- Apache Tika
- OCR 服务
- 自研 parser pipeline

---

## 3.2 Chunking 策略

要掌握：

- 固定长度分块
- 按标题分块
- 语义分块
- parent-child chunk
- sliding window
- table-aware chunking
- code-aware chunking
- metadata-aware chunking

关键认知：

> Chunking 不是越小越好，也不是越大越好，而是要服务于检索和回答。

---

## 3.3 Embedding 与向量库

需要掌握：

- embedding model 选择
- 向量维度
- cosine similarity
- dot product
- approximate nearest neighbor
- index 类型
- metadata filtering
- 多租户隔离
- 增量更新

推荐向量存储：

| 场景           | 推荐                         |
| -------------- | ---------------------------- |
| 快速原型       | pgvector                     |
| 中小企业项目   | Qdrant                       |
| 大规模向量检索 | Milvus                       |
| 搜索系统融合   | Elasticsearch / OpenSearch   |
| 云原生托管     | Pinecone / Weaviate Cloud 等 |

---

## 3.4 高级检索

必须掌握：

- BM25
- dense retrieval
- sparse retrieval
- hybrid search
- rerank
- query rewrite
- multi-query retrieval
- hypothetical document embedding
- metadata filtering
- time-aware retrieval
- permission-aware retrieval

Rerank 在企业 RAG 中非常重要。典型流程是：

```text
先召回 top 50
 -> rerank 到 top 5~10
 -> 组装上下文
 -> 生成答案
```

---

## 3.5 RAG 权限控制

这是 Java 后端开发者的优势区。

你要做到：

- tenant_id 隔离
- user_id / role / department 权限
- document-level ACL
- chunk-level metadata
- retrieval 前权限约束
- retrieval 后二次权限校验
- 权限变更后的索引更新
- 审计日志
- 引用来源校验

不要只依赖一句：

```text
where metadata.user_id = current_user
```

生产系统里还要考虑：

- 用户角色变化
- 文档权限变化
- 共享链接
- 部门继承权限
- 历史缓存泄露
- 多租户数据混查
- Prompt Injection 绕过权限

---

## 3.6 RAG 评估

你需要建立评估集：

```text
问题
标准答案
相关文档
允许引用范围
不可回答情况
```

指标包括：

- retrieval recall
- precision@k
- MRR
- nDCG
- answer relevance
- faithfulness
- groundedness
- citation accuracy
- refusal correctness

RAGAS 仍然值得学，它的目标是为 RAG 和 Agentic workflow 提供系统化评估能力。([LangChain 文档][4])

## 阶段项目

做一个 **企业级权限隔离知识库系统**。

功能要求：

- 用户登录
- 多租户
- 文件上传
- 文档解析
- 权限设置
- embedding 入库
- hybrid search
- rerank
- 带引用回答
- 无答案时拒答
- 管理后台
- eval 面板
- 调用链 tracing

## 推荐技术栈

```text
Java:
Spring Boot
Spring Security
Spring AI
PostgreSQL
Redis
Kafka / RabbitMQ
OpenTelemetry

Python:
文档解析 worker
embedding batch job
RAGAS eval script

存储:
PostgreSQL + pgvector / Qdrant / Milvus
S3 / MinIO
Elasticsearch / OpenSearch
```

## 阶段验收标准

你应该能做到：

- 用户只能检索自己有权限的文档
- 答案必须带引用
- 没有依据时拒答
- 可以看到每次检索命中的 chunk
- 可以评估一次改动是否让 RAG 变好或变差

---

# 阶段 4：Agent 与可控工作流

## 目标

从聊天机器人升级为能调用工具、执行流程、处理复杂任务的 AI 系统。

但要记住：

> 生产级 Agent 不是“让模型自由发挥”，而是“用代码和状态机约束模型”。

---

## 4.1 Function Calling / Tool Calling

你要掌握：

- tool schema 设计
- tool 参数校验
- tool result 结构化
- tool error handling
- tool retry
- tool timeout
- tool permission
- tool audit

典型工具：

- 查询数据库
- 搜索知识库
- 查询订单
- 创建工单
- 发送邮件
- 调用内部 API
- 读取日志
- 创建报表

---

## 4.2 Agent 基本模式

需要理解：

- ReAct
- planner-executor
- evaluator-optimizer
- router agent
- supervisor-worker
- reflection
- self-correction

但不要迷信“多 Agent”。

正确顺序是：

```text
单模型结构化输出
 -> 单 Agent 多工具
 -> 状态机工作流
 -> human-in-the-loop
 -> 多 Agent 协作
```

---

## 4.3 状态机与工作流

生产级 Agent 应该有清晰状态：

```text
START
 -> classify_intent
 -> retrieve_context
 -> plan
 -> call_tool
 -> validate_result
 -> ask_human_if_needed
 -> generate_response
 -> END
```

推荐工具：

- LangGraph
- LlamaIndex Workflows
- Spring AI + 自研 workflow
- Temporal
- Camunda
- Netflix Conductor

LangGraph 的定位正适合这类场景：它强调 durable execution、human-in-the-loop、长期运行任务、状态持久化和 memory。([LangChain 文档][5])

---

## 4.4 Human-in-the-loop

以下操作不应该让 Agent 自动执行：

- 发邮件
- 删除文件
- 修改数据库
- 提交代码
- 创建订单
- 退款
- 变更权限
- 操作生产环境

应该设计审批机制：

```text
Agent 生成建议
 -> 用户确认
 -> 系统执行
 -> 记录审计日志
```

LangChain / LangGraph 相关文档也把 human oversight 用于敏感工具调用，例如执行 SQL 或写文件前暂停等待人工确认。([LangChain 文档][6])

---

## 阶段项目

做一个 **多工具工单处理 Agent**。

功能：

- 读取 Jira / 邮件 / 工单
- 判断问题类型
- 检索知识库
- 查询日志
- 查询 GitLab / GitHub issue
- 生成分析报告
- 推荐处理方案
- 人工确认后更新工单状态或发送回复

## 阶段验收标准

你应该能做到：

- Agent 每一步状态可追踪
- 工具调用有权限控制
- 失败可以恢复
- 长任务不会因为进程重启丢失
- 高风险操作需要人工确认
- 每次 Agent 决策有日志和审计

---

# 阶段 5：MCP 与企业系统集成

## 目标

掌握 2026 年 AI 应用连接外部工具和企业系统的重要协议。

MCP 的官方规范将其定义为一种开放协议，用于让 LLM 应用与外部数据源和工具进行标准化集成。([模型上下文协议][7])
2026 年 MCP Roadmap 也明确把 transport scalability、agent communication、governance 和 enterprise readiness 作为重点方向。([Model Context Protocol Blog][8])

---

## 5.1 你要理解 MCP 解决什么问题

没有 MCP 时：

```text
每个模型客户端都要单独适配 GitHub、Slack、DB、文件系统、ERP
```

有 MCP 后：

```text
AI Client <-> MCP Server <-> 企业系统 / 数据源 / 工具
```

MCP 把工具、资源、Prompt 等能力标准化。

---

## 5.2 MCP 核心概念

你需要掌握：

- MCP Client
- MCP Server
- Tools
- Resources
- Prompts
- Sampling
- Transport
- STDIO
- HTTP / Streamable HTTP
- 权限与鉴权
- 工具描述
- 工具调用返回格式

---

## 5.3 Java 后端应该怎么用 MCP

非常适合 Java 后端的方向：

- 用 Spring Boot 封装内部系统为 MCP Server
- 把 MySQL 查询包装成安全只读工具
- 把 ERP 查询包装成业务工具
- 把工单系统包装成 MCP 工具
- 把内部权限系统接入 MCP Server
- 做 MCP Gateway

Spring AI 已经提供 MCP 相关支持，适合 Spring 生态接入 MCP Client / Server。([Home][1])

---

## 5.4 MCP 安全

这是重点。

MCP 不是简单“把数据库暴露给 AI”。你必须做：

- tool allowlist
- OAuth / token scope
- 用户身份透传
- resource-level permission
- command whitelist
- 参数校验
- SQL AST 校验
- 只读 / 写操作分离
- 写操作审批
- 审计日志
- 沙箱执行
- rate limit
- 防 Prompt Injection
- 防命令注入
- 防供应链污染

尤其要谨慎 STDIO 和本地命令执行类 MCP Server。近期已有关于 MCP SDK / STDIO 处理引发远程代码执行风险的安全报道，说明 MCP 工程化必须把安全作为核心能力。([Tom's Hardware][9])

## 阶段项目

做一个 **企业内部系统 MCP Gateway**。

功能：

- 暴露用户查询工具
- 暴露订单查询工具
- 暴露工单查询工具
- 暴露知识库搜索工具
- 支持 OAuth
- 支持 tool allowlist
- 支持审计日志
- 所有写操作需要人工确认
- 可被 Agent 客户端调用

## 阶段验收标准

你应该能做到：

- 设计安全的 MCP Tool Schema
- 不把敏感 API 直接暴露给模型
- 每次工具调用可审计
- 不同用户看到不同工具和资源
- 高危工具必须审批

---

# 阶段 6：Text-to-SQL 与数据分析 Copilot

## 目标

掌握一个高价值但高风险的 AI 应用方向。

不要一开始就做“随便问数据库”。正确方向是：

> 企业 BI Copilot：自然语言问题 -> 语义层 -> SQL 生成 -> 安全校验 -> 查询 -> 图表解释。

---

## 核心能力

### 1. Schema 理解

需要处理：

- 表结构
- 字段含义
- 外键关系
- 指标口径
- 时间字段
- 枚举值
- 数据权限

### 2. SQL 安全

必须做：

- 只允许 SELECT
- 禁止 DDL / DML
- SQL AST parse
- LIMIT 注入
- timeout
- explain cost check
- 表级权限
- 行级权限
- 字段脱敏
- query audit

### 3. 语义层

不要让模型直接面对复杂数据库。

建议加入：

- 指标定义
- 维度定义
- 可查询表白名单
- business glossary
- 示例 SQL
- 查询模板

### 4. 错误修复

Agent 可以做：

```text
生成 SQL
 -> 校验
 -> 执行
 -> 报错
 -> 修复
 -> 再执行
```

但要限制重试次数，并记录每次修改。

## 阶段项目

做一个 **安全 Text-to-SQL BI 助手**。

功能：

- 用户自然语言提问
- 系统识别指标
- 生成 SQL
- SQL 安全校验
- 查询分析库
- 生成图表
- 解释结果
- 给出 SQL 和数据来源
- 高成本查询拦截

## 阶段验收标准

你应该能做到：

- 不会执行危险 SQL
- 不会越权查数据
- SQL 生成失败可诊断
- 查询结果可解释
- 所有查询可审计

---

# 阶段 7：LLMOps、评估与上线运维

## 目标

从“能跑 Demo”升级为“能上线、能监控、能迭代”。

---

## 7.1 Tracing

每次 AI 调用都要记录：

- user id
- request id
- model
- prompt version
- input tokens
- output tokens
- latency
- cost
- retrieved chunks
- tool calls
- tool latency
- final answer
- error
- user feedback

推荐工具：

- OpenTelemetry
- Langfuse
- Arize Phoenix
- Helicone
- Weights & Biases
- vendor tracing

---

## 7.2 Evals

必须建立：

- prompt eval
- RAG eval
- agent eval
- regression eval
- safety eval
- latency eval
- cost eval

你应该能回答：

```text
这次改 Prompt 后效果是变好了还是变差了？
换 embedding 模型后检索召回有没有提升？
rerank top_k 从 5 改到 10 是否值得？
换模型后成本下降了多少，质量损失多少？
```

---

## 7.3 成本控制

要做：

- token 预算
- prompt 压缩
- cache
- model routing
- cheap model first
- expensive model fallback
- batch processing
- streaming early stop
- max tool iterations
- rate limit

---

## 7.4 安全

必须掌握：

- Prompt Injection
- Jailbreak
- 数据泄露
- PII 脱敏
- 越权检索
- 工具误调用
- SQL 注入
- 命令注入
- SSRF
- 文件读取风险
- Agent runaway
- 审计与告警

## 阶段项目

给前面所有项目加一个 **AI Observability Dashboard**：

功能：

- 调用量
- 成本
- 延迟
- 错误率
- 模型分布
- 工具调用链
- RAG 命中 chunk
- 用户反馈
- eval 分数
- prompt version 对比

## 阶段验收标准

你应该能做到：

- 线上问题可回放
- prompt 改动可灰度
- 模型切换可评估
- 成本异常可报警
- 质量下降可发现

---

# 阶段 8：多模态 AI 应用能力

## 目标

补齐 2026 年 AI 应用常见的多模态需求。

你不一定要做算法，但要会调用和集成。

## 需要掌握

### 文档多模态

- PDF 页面截图理解
- 图表问答
- 表格识别
- OCR
- 发票识别
- 合同审查
- PPT 总结

### 图片理解

- 图片分类
- 图片描述
- UI 截图分析
- 商品识别
- 质检识别

### 语音

- ASR
- TTS
- 实时语音对话
- 会议纪要
- 客服质检

### 视频

- 视频摘要
- 镜头切分
- 内容审核
- 短视频理解

## 阶段项目

做一个 **多模态企业文档助手**：

- 上传 PDF / 图片 / 表格
- 自动识别结构
- 提取关键信息
- 支持问答
- 支持引用页码
- 支持表格转结构化数据

---

# 阶段 9：综合毕业项目

建议你最终做一个完整项目，而不是一堆零散 Demo。

## 推荐毕业项目：企业 AI 助手平台

### 功能模块

1. 用户登录与权限系统
2. 企业知识库 RAG
3. 多租户文件管理
4. MCP 工具网关
5. 工单处理 Agent
6. Text-to-SQL BI 助手
7. Human-in-the-loop 审批
8. AI 调用观测平台
9. Eval 管理后台
10. 成本与限流系统

### 架构示意

```text
Frontend
  |
API Gateway
  |
Spring Boot AI Backend
  |-- Auth / RBAC
  |-- AI Gateway
  |-- RAG Service
  |-- Agent Workflow Service
  |-- MCP Gateway
  |-- Audit Service
  |
PostgreSQL / Redis / Kafka
  |
Vector DB / Search Engine
  |
Python Workers
  |-- Document Parsing
  |-- Embedding
  |-- Evaluation
  |
LLM Providers
```

### 技术栈建议

```text
Backend:
Java 21+
Spring Boot
Spring AI
Spring Security
Spring WebFlux
PostgreSQL
Redis
Kafka / RabbitMQ
OpenTelemetry

AI / Data:
Python
FastAPI
Pydantic
LlamaIndex
LangGraph
RAGAS
pandas

Search / Vector:
Qdrant / Milvus / pgvector
Elasticsearch / OpenSearch

Infra:
Docker
Kubernetes
MinIO / S3
Prometheus
Grafana

Frontend:
React / Next.js
```

---

# 推荐学习顺序

## 第 1 个月：模型 API 与 Spring AI

目标：做出 AI Gateway。

学习：

- OpenAI / Anthropic / Gemini API
- streaming
- structured output
- tool calling
- Spring AI ChatClient
- Spring Boot 封装统一 AI 接口

产出：

- 多模型 AI Gateway
- 结构化输出 Demo
- 流式聊天 Demo

---

## 第 2-3 个月：RAG 系统

目标：做出企业知识库。

学习：

- 文档解析
- chunking
- embedding
- vector DB
- hybrid retrieval
- rerank
- ACL 权限过滤
- citation
- RAG eval

产出：

- 多租户权限隔离知识库
- 带引用回答
- 检索日志
- 初版 eval 集

---

## 第 4 个月：Agent 与 Workflow

目标：做出可控 Agent。

学习：

- tool calling
- LangGraph
- 状态机
- human-in-the-loop
- 长任务
- 审批机制

产出：

- 工单处理 Agent
- 工具调用审计
- 人工确认流程

---

## 第 5 个月：MCP 与企业集成

目标：做出 MCP Gateway。

学习：

- MCP Client / Server
- Spring AI MCP
- tool schema
- 权限控制
- MCP 安全

产出：

- 内部系统 MCP Server
- Agent 调用 MCP 工具
- 工具权限和审计

---

## 第 6 个月：LLMOps 与综合项目

目标：把系统做成可展示的作品集。

学习：

- tracing
- evals
- cost control
- prompt versioning
- model routing
- safety test

产出：

- AI Observability Dashboard
- Eval Dashboard
- 综合企业 AI 助手平台

---

# 哪些内容可以暂时不学？

以下内容不是第一优先级：

| 内容                    | 原因                                   |
| ----------------------- | -------------------------------------- |
| 从零训练大模型          | 成本极高，不适合应用开发转型初期       |
| 深度微调                | 多数业务先用 RAG、Prompt、工具调用解决 |
| 复杂多 Agent 自主协作   | 成本高、调试难、生产风险大             |
| 本地部署大模型          | 除非你目标是私有化部署岗位             |
| 过度研究 LangChain LCEL | 有用，但不是 2026 主线                 |
| 炫技 Prompt 模板        | 不如学结构化输出和 eval                |
| 纯算法论文复现          | 对 AI 应用开发帮助有限                 |

---

# 你应该重点打造的能力标签

转型后，你的简历上应该呈现这些关键词：

```text
Java AI Application Engineer
Spring AI
LLM Gateway
Structured Outputs
Function Calling
RAG
Hybrid Search
Rerank
Vector Database
MCP Server
Agent Workflow
LangGraph
Human-in-the-loop
LLMOps
RAG Evaluation
Prompt Injection Defense
Enterprise AI Integration
```

而不是只写：

```text
会 LangChain
会 Prompt
会调用 OpenAI API
```

---

# 最终路线总结

你的转型方向应该是：

```text
Java 后端
 -> AI Gateway
 -> 企业 RAG
 -> Agent Workflow
 -> MCP 企业集成
 -> LLMOps / Evals / 安全
 -> 企业级 AI 应用架构师
```

最值得投入的三类项目是：

1. **权限隔离企业知识库**
2. **工单处理 Workflow Agent**
3. **安全 Text-to-SQL BI 助手**

其中第一个最适合入门和求职展示，第二个最能体现 Agent 工程能力，第三个最能体现业务价值和后端安全能力。

一句话概括：

**2026 年 Java 后端转 AI 应用开发，核心不是转语言，而是把你原来的后端工程能力迁移到“模型 + 数据 + 工具 + 权限 + 评估 + 运维”的新架构里。**

[1]: https://docs.spring.io/spring-ai/reference/index.html?utm_source=chatgpt.com "Introduction :: Spring AI Reference"
[2]: https://developers.openai.com/api/docs/guides/migrate-to-responses?utm_source=chatgpt.com "Migrate to the Responses API"
[3]: https://developers.openai.com/api/docs/guides/structured-outputs?utm_source=chatgpt.com "Structured model outputs | OpenAI API"
[4]: https://docs.langchain.com/oss/python/langgraph/durable-execution?utm_source=chatgpt.com "Durable execution - Docs by LangChain"
[5]: https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com "LangGraph overview - Docs by LangChain"
[6]: https://docs.langchain.com/oss/python/langchain/human-in-the-loop?utm_source=chatgpt.com "Human-in-the-loop - Docs by LangChain"
[7]: https://modelcontextprotocol.io/specification/2025-03-26?utm_source=chatgpt.com "Specification"
[8]: https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/?utm_source=chatgpt.com "The 2026 MCP Roadmap | Model Context Protocol Blog"
[9]: https://www.tomshardware.com/tech-industry/artificial-intelligence/anthropics-model-context-protocol-has-critical-security-flaw-exposed?utm_source=chatgpt.com "Anthropic's Model Context Protocol includes a critical remote code execution vulnerability - newly discovered exploit puts 200,000 AI servers at risk"
