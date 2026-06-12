# 对 Java 后端来说，应该怎么理解 LLM

你可以把 LLM 看成一个新的“智能服务组件”。

传统 Java 后端：

```text
Controller
→ Service
→ Repository
→ Database
```

Agent 后端：

```text
Controller
→ Agent Service
→ LLM Client
→ Tool Registry
→ RAG Retriever
→ Workflow Engine
→ Business Services
→ Database
```

也就是说，LLM 不替代后端工程。

它是后端系统里的一个能力模块。

你仍然需要：

- 接口设计
- 权限校验
- 事务控制
- 日志
- 测试
- 监控
- 部署
- 限流
- 异常处理
- 数据一致性

LLM 只是在其中负责过去很难写死规则的部分：

- 自然语言理解
- 任务拆解
- 文本生成
- 语义判断
- 复杂上下文整合
