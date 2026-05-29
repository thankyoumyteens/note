# 第 12 课：Spring AI RAG 适配课

你在第 11 课已经手写完成了最小 RAG 闭环：

```text
文档上传
  -> 文本切分
  -> embedding
  -> pgvector 入库
  -> top-k 检索
  -> LLM 基于 context 回答
```

第 12 课的目标不是重写第 11 课，而是理解 Spring AI 对 RAG 的抽象：

```text
EmbeddingModel
VectorStore
Document
SearchRequest
Advisor / RAG API
```

一句话概括：

> 本课在不替换主线 RAG 的前提下，做一个 Spring AI RAG Demo，理解 Spring AI 如何封装 embedding、vector store 和 retrieval 流程。
