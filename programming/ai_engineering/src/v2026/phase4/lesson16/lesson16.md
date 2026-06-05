# 第 16 课：Agent Workflow 入门

前面你已经有：

```text
AI Gateway
Tool Calling 基础
RAG
权限隔离 RAG
Context Engineering
工具结果摘要
限流与日志
```

现在可以进入 Agent，但本课不能一上来做“自由循环 Agent”。企业系统更常见、更可靠的方式是：

```text
状态机 + 有限步骤 + 可恢复 + 可人工介入
```

一句话概括：

> 本课实现一个最小 Workflow Agent：用状态机处理工单，支持任务拆解、步骤执行、失败恢复、human-in-the-loop 和 agent step 次数限制。
