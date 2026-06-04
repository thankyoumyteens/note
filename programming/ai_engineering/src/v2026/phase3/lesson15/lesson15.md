# 第 15 课：Context Engineering

前面你已经有：

```text
AI Gateway
结构化输出
Tool Calling
Evals
生产化日志与限流
RAG
RAG 质量增强
权限隔离 RAG
```

但现在还有一个问题：**模型上下文窗口不是无限的**。

如果你把所有内容都塞进 prompt，会出现：

```text
token 成本高
响应变慢
超过模型上下文窗口
RAG chunks 太多
工具结果太长
对话历史太长
模型注意力分散
```

一句话概括：

> 本课给 AI Gateway 增加上下文治理能力：估算 token、控制上下文预算、压缩长文本、摘要工具结果，并为后续 Agent Workflow 做准备。
