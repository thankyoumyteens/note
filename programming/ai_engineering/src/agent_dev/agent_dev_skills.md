# Agent 开发的招聘要求

## 1. Java / Python

需要掌握：

- Java：Spring Boot、Spring Cloud、MyBatis、微服务开发
- Python：基础语法、工程化代码、FastAPI / Flask / Django
- Shell / Linux：基础脚本、部署、日志排查
- TypeScript / 前端：部分岗位要求 Vue / React，至少能看懂并配合联调
- 代码规范、异常处理、单元测试、集成测试、性能分析

## 2. 后端工程与分布式系统

需要掌握：

- 微服务架构设计
- 高并发、高可用、高性能系统设计
- 分布式系统基础
- 服务治理、接口设计、限流、熔断、降级
- MySQL / PostgreSQL 使用与性能优化
- Redis、Kafka 等中间件
- Linux 服务器基础操作
- CI/CD 流水线
- Docker / Kubernetes 部署
- 多租户隔离、稳定性保障、监控告警

## 3. LLM 应用开发基础

需要掌握：

- LLM 基本原理与能力边界
- GPT、Claude、Llama 等主流模型差异
- 模型 API 调用与集成
- Streaming / SSE 流式输出
- Token、上下文窗口、成本、延迟控制
- 多轮对话设计
- 结构化输出
- 模型结果稳定性与可控性

## 4. Prompt Engineering

需要掌握：

- Prompt 模板设计
- 复杂指令链 Prompt Chain
- 角色设定、任务约束、输出格式约束
- 用户意图拆解
- 业务意图表达
- 高转化率 Prompt 设计
- Prompt A/B 测试
- Prompt 版本管理
- 根据评估结果持续优化 Prompt

## 5. Context Engineering 上下文工程

需要掌握：

- 长上下文管理
- 短期记忆与长期记忆
- 多轮对话状态维护
- 上下文压缩与摘要
- 工具调用结果写入上下文
- 用户画像 / 个性化上下文
- RAG 结果与历史对话的组合策略
- 防止上下文污染
- 控制模型只基于可靠上下文回答

## 6. AI Agent 架构设计

需要掌握：

- Agent 基本架构
- Planner / Executor / Tool / Memory / Runtime 设计
- ReAct 模式
- 任务规划 Task Planning
- 多步骤任务工作流 Workflow
- Agent 状态管理
- 任务拆解与执行链路
- Human-in-the-loop 人工确认机制
- Agent Runtime 抽象
- Tool / Memory / Context 抽象
- Agent 失败恢复与容错机制

## 7. Tool Calling / Function Calling

需要掌握：

- Function Calling 原理
- Tool Schema 设计
- 工具参数生成与校验
- 工具调用权限控制
- 工具调用失败重试
- 工具调用日志记录
- 工具调用结果解析
- 外部 API 集成
- 企业内部系统对接，例如 Jira、飞书、KMS、PLM、业务系统 API
- 防止模型乱调用工具

## 8. Workflow 编排与状态机

需要掌握：

- 多步骤任务流设计
- 固定工作流与动态工作流的区别
- LangGraph 状态图思想
- 节点、边、状态、条件分支
- 任务重试、跳转、终止
- Agent 执行轨迹记录
- 工作流可观测性
- 工作流异常处理
- 工作流模板复用

## 9. RAG 知识库系统

需要掌握：

- 文档解析
- 文档切分 Chunking
- Embedding 模型选型
- 向量化流程
- 向量数据库使用
- 向量检索
- 关键词检索
- 混合检索 Hybrid Search
- Query Rewrite 查询改写
- Recall 召回优化
- Rerank 重排序
- 上下文拼接策略
- RAG 结果评估
- 知识库更新与版本管理

## 10. 向量数据库与检索系统

需要掌握：

- Milvus
- pgvector
- Chroma
- FAISS
- Pinecone
- Elasticsearch
- 倒排索引
- 语义检索
- 向量召回
- 多路召回
- 重排序模型
- 检索效果评测
- 检索延迟优化

## 11. Agent 框架与平台

需要掌握：

- LangChain
- LangGraph
- LlamaIndex
- AutoGen
- Dify
- Coze
- Flowise
- n8n
- FastGPT
- AgentScope
- MetaGPT

其中最值得优先学的是：

- LangChain：LLM 应用基础框架
- LangGraph：Agent 工作流与状态管理
- LlamaIndex：RAG / 数据连接 / 检索增强
- Dify：低代码 Agent 产品落地
- AutoGen：多 Agent 协作

## 12. MCP / Skills / Agent 协议生态

需要掌握：

- MCP 基本概念
- MCP Server / MCP Client
- Tools 暴露方式
- 企业内部数据源连接
- 标准化连接器
- Skills 机制
- A2A / Agent-to-Agent 基本思想
- 多 Agent 之间的任务分发与协作
- Agent 安全接入机制
- OpenClaw、AutoGPT、BabyAGI、Hermes-Agent 等开源项目的基本思路

## 13. 多 Agent 协作

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

## 14. Agent 评估与优化

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
- 成本、延迟、稳定性优化

## 15. AI Coding / Vibe Coding 工具

需要掌握：

- Claude Code
- OpenAI Codex / Codex CLI
- GitHub Copilot
- Cursor
- OpenCode
- 用 AI 工具完成完整项目
- 用 AI 生成代码、重构代码、补测试
- 用 AI 阅读项目结构
- 用 AI 定位 bug
- 用 AI 生成技术文档
- AI 过度发挥的识别与控制
- AI 工具权限与安全边界

## 16. 产品落地与业务集成能力

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

## 17. 模型训练、微调与算法能力

需要掌握：

- 基础机器学习
- 基础深度学习
- PyTorch
- sklearn
- Fine-tuning 微调
- 模型量化
- 模型部署
- 垂直领域模型优化
- 多模态模型基础
- CV + Agent 结合
- 训练数据构建
- 测试集构建
- 数据质量评估

这部分多数是加分项，不是所有 Agent 应用开发岗位的硬性主线。

## 18. 安全、权限与稳定性

需要掌握：

- Tool 权限控制
- 数据访问权限
- 企业内部系统安全接入
- Prompt Injection 防护
- RAG 数据污染防护
- 敏感信息过滤
- 日志脱敏
- 容错机制
- 降级策略
- 高并发下的稳定性保障
- 成本控制
- 监控告警
