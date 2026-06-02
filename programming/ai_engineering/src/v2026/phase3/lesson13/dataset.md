# 创建 RAG eval 数据集

用小型测试集评估 RAG 是否真的变好，而不是凭感觉。

RAG eval 最基础可以先看三件事：

```text
是否检索到正确 chunk
回答是否包含关键答案
无答案问题是否拒答
```

#### 代码

文件：

```text
python-tools/rag_eval_cases.jsonl
```

内容示例：

```jsonl
{"id":"rag-001","question":"RAG 的核心思想是什么？","expectedAnswerContains":"先从外部知识库中检索相关内容","shouldHaveAnswer":true}
{"id":"rag-002","question":"RAG 能解决什么问题？","expectedAnswerContains":"降低模型幻觉","shouldHaveAnswer":true}
{"id":"rag-003","question":"文档里有没有提到 Kubernetes？","expectedAnswerContains":"根据已提供文档无法确定","shouldHaveAnswer":false}
```

#### 代码说明

这是最小版 eval，不是最终版 RAGAS。
