# Agent 开发学习路线大纲

## 前置基础：Java / Python / 后端工程基础

需要掌握：

- Java 后端开发：Spring Boot、Spring Cloud、MyBatis、REST API、异常处理、单元测试、集成测试
- Python 工程基础：Python 3.13、uv、基础语法、工程化代码、FastAPI / Flask / Django
- Shell / Linux：基础脚本、日志排查、进程管理、部署基础
- 后端工程能力：接口设计、数据库设计、缓存、中间件、性能分析
- 分布式基础：微服务、高并发、高可用、限流、熔断、降级
- 数据库与中间件：MySQL / PostgreSQL、Redis、Kafka
- 部署与运维：Docker、Kubernetes、CI/CD、监控告警
- 前端协作能力：TypeScript、Vue / React 基础，能看懂前端代码并配合联调

---

## LLM 应用开发基础

需要掌握：

- LLM 基本原理与能力边界
- OpenAI、DeepSeek、Claude 的 API 调用方式
- 多 provider 路由设计
- API Key 管理与环境变量配置
- 请求参数：model、messages、temperature、max_tokens、stream
- system / user / assistant 消息结构
- 统一请求结构与统一响应结构
- 错误处理：400、401、403、429、5xx
- 超时、重试、fallback、provider 降级
- Token usage 记录与成本估算

---

## Streaming / SSE 与统一响应协议

需要掌握：

- Streaming 与 SSE 的基本概念
- OpenAI-compatible streaming 事件解析
- Claude Messages streaming 事件解析
- 使用 Java 和 Python 实现 SSE
- 前端 fetch + ReadableStream 接收 POST SSE
- 后端统一封装前端事件协议
- message / error / done 事件设计
- 代理缓冲、超时、断流、错误事件处理

---

## Prompt 与结构化输出

需要掌握：

- Prompt 模板设计
- 角色设定、任务约束、输出格式约束
- Few-shot 示例设计
- 用户意图拆解与任务说明
- 结构化输出：JSON、Schema、枚举、字段约束
- 输出稳定性控制
- Prompt 版本管理
- Prompt A/B 测试与持续优化

---

## Tool Calling / Function Calling

需要掌握：

- Function Calling / Tool Calling 原理
- Tool Schema 设计
- 工具参数生成与校验
- 工具调用权限控制
- 工具调用失败重试
- 工具调用日志记录
- 工具调用结果解析与摘要
- 外部 API 集成
- 企业内部系统对接，例如 Jira、飞书、KMS、PLM、业务系统 API
- 防止模型乱调用工具

---

## Context Engineering

需要掌握：

- Token 预算、上下文窗口、成本与延迟控制
- 上下文来源、优先级与组织结构
- 长上下文压缩、摘要与截断
- 对话状态、短期记忆与长期记忆
- 用户画像与个性化上下文
- RAG、工具结果与历史对话的组合策略
- 上下文选择、排序、裁剪与可信度标注
- 上下文冲突处理、污染防护与可靠回答边界

---

## RAG 知识库系统

需要掌握：

- 文档解析：PDF、Word、Markdown、HTML、网页、表格
- 文档切分 Chunking 与 overlap 策略
- Embedding 模型选型
- 向量化流程
- 向量数据库：pgvector、Milvus、Chroma、FAISS、Pinecone
- 关键词检索与 Elasticsearch
- 混合检索 Hybrid Search
- Query Rewrite 查询改写
- Recall 召回优化
- Rerank 重排序
- 上下文拼接策略
- RAG 结果评估
- 知识库更新、权限、版本管理

---

## Workflow / 状态机 / LangGraph 思想

需要掌握：

- 多步骤任务流设计
- 固定工作流与动态工作流的区别
- 状态机基本思想
- LangGraph 状态图思想
- 节点、边、状态、条件分支
- 任务重试、跳转、终止
- 执行轨迹记录
- 工作流异常处理
- 工作流模板复用

---

## Agent 架构设计

需要掌握：

- Agent 基本架构
- Planner / Executor / Tool / Memory / Runtime 设计
- ReAct 模式
- 任务规划 Task Planning
- 任务拆解与执行链路
- Agent 状态管理
- Human-in-the-loop 人工确认机制
- Agent Runtime 抽象
- Tool / Memory / Context 抽象
- Agent 失败恢复与容错机制

---

## Eval / Trace / Observability / LLMOps

需要掌握：

- 准确率评估
- 任务完成率评估
- 响应延迟评估
- 工具调用成功率评估
- RAG 命中率评估
- 召回率、精确率
- 自动化测试集构建
- 标注规范设计
- 回归测试
- LLM-as-Judge
- 失败案例分析
- Agent 执行链路 Trace
- Prompt log、tool trace、conversation replay
- 成本、延迟、稳定性指标

---

## 安全、权限、成本、稳定性

需要掌握：

- Tool 权限控制
- 数据访问权限
- 企业内部系统安全接入
- Prompt Injection 防护
- RAG 数据污染防护
- 敏感信息过滤
- 日志脱敏
- API Key 保护
- 限流、熔断、降级
- 超时、重试、fallback
- 高并发下的稳定性保障
- Token 配额、成本限额、Agent step 限制
- 监控告警与审计

---

## Agent 框架与平台

需要掌握：

- LangChain：LLM 应用基础框架
- LangGraph：Agent 工作流与状态管理
- LlamaIndex：RAG / 数据连接 / 检索增强
- Dify：低代码 Agent 产品落地
- AutoGen：多 Agent 协作
- Coze、Flowise、n8n、FastGPT：低代码 / 工作流平台
- AgentScope、MetaGPT：Agent 框架了解

优先级：

- 主线优先：LangChain、LangGraph、LlamaIndex、Dify
- 了解加分：AutoGen、Coze、Flowise、n8n、FastGPT、AgentScope、MetaGPT

---

## MCP / Skills / 协议生态

需要掌握：

- MCP 基本概念
- MCP Server / MCP Client
- Tools 暴露方式
- 企业内部数据源连接
- 标准化连接器
- Skills 机制
- A2A / Agent-to-Agent 基本思想
- Agent 安全接入机制
- OpenClaw、AutoGPT、BabyAGI、Hermes-Agent 等开源项目的基本思路

---

## 多 Agent 协作

需要掌握：

- 多 Agent 分工
- Coordinator / Worker 模式
- Supervisor Agent
- 专家 Agent
- Agent 之间的信息传递
- Agent 协作协议
- 冲突处理
- 任务分派
- 多 Agent 状态同步
- 多 Agent 成本与延迟控制

---

## 产品落地与业务集成

需要掌握：

- 从业务需求拆解 Agent 方案
- 智能客服场景
- 企业知识库场景
- 办公自动化场景
- 金融问答 / 投研 / 财富工具场景
- 汽车研发流程场景
- 健康管理场景
- 企业内部流程自动化
- 与前端、后端、算法、产品团队协作
- 技术方案设计
- 技术文档输出
- 组件沉淀与模板复用

---

## 模型训练 / 微调 / 多模态加分项

需要掌握：

- 基础机器学习
- 基础深度学习
- PyTorch、sklearn
- Fine-tuning 微调
- 模型量化
- 模型部署
- 垂直领域模型优化
- 多模态模型基础
- CV + Agent 结合
- 训练数据构建
- 测试集构建
- 数据质量评估
