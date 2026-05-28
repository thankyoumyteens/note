# 第 11 课：RAG 基础系统

前面你已经有：

```text
Java AI Gateway
LlmClient
Embedding 前的模型调用基础
Python 工具链
Evals 基础
生产化基础能力
```

现在开始做第一个真正的 AI 应用核心模块：**RAG 问答系统**。

一句话概括：

> 本课实现一个最小 RAG 系统：上传文档 → 切分 chunk → 调 embedding → 存入 pgvector → 查询时 top-k 检索 → 把 context 塞给 LLM 回答。
