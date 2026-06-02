# 第 13 课：RAG 质量增强

第 11 课你已经跑通了最小 RAG：

```text
文档上传 -> chunk -> embedding -> pgvector -> top-k 检索 -> LLM 回答
```

但最小 RAG 有几个明显问题：

```text
只靠向量检索，关键词命中不稳定
模型可能在 context 不足时硬答
回答里没有引用来源
无法评估 RAG 效果好坏
没有系统比较 pgvector / Qdrant / Milvus / OpenSearch
```

一句话概括：

> 本课把最小 RAG 升级成 RAG v2：增加 query rewrite、hybrid search、no-answer 判断、citation 返回、基础 RAG eval，并建立后续更强向量数据库的评估清单。
