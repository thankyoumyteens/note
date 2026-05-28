# 向量数据库是什么

**向量数据库**就是专门用来存储和检索 **embedding 向量** 的数据库。

## 为什么普通数据库不够？

普通关系型数据库擅长：

```sql
WHERE name = '张三'
WHERE status = 'PAID'
WHERE created_at > '2026-01-01'
```

也就是精确匹配、范围查询、关联查询。

但 RAG 需要的是：找出和 “怎么减少大模型胡编？” 语义最接近的文档片段。

文档里可能写的是：

```text
RAG 可以降低模型幻觉。
```

这里没有“胡编”这个关键词，但语义接近。普通 SQL 不擅长这种语义相似度搜索。

向量数据库擅长：

```text
给我找出和这个问题向量最接近的 5 个文档 chunk。
```

也就是：

```text
top-k similarity search
```

## 它在 RAG 里怎么工作？

文档入库时：

```text
文档
  -> 切成 chunk
  -> 每个 chunk 调 embedding 模型
  -> 得到向量
  -> 存进向量数据库
```

用户提问时：

```text
用户问题
  -> 调 embedding 模型
  -> 得到问题向量
  -> 去向量数据库找最相似的 top-k chunk
  -> 把这些 chunk 塞给大模型回答
```

## 一个简单类比

你可以把向量数据库想成一个“语义地图”。

```text
“RAG 可以降低模型幻觉”
“检索增强生成能减少胡编”
“先查资料再回答可以提升准确性”
```

这些句子意思接近，所以它们在向量空间里的位置比较近。

而：

```text
“今天午饭吃什么”
```

和它们语义无关，位置就比较远。

向量数据库的任务就是：

```text
在这个语义地图里，快速找到离用户问题最近的内容。
```

## 第 11 课为什么用 pgvector？

因为你是 Java 后端路线，已经熟悉关系型数据库。用 PostgreSQL + pgvector 可以同时保存：

```text
文档元信息
chunk 内容
embedding 向量
创建时间
documentId
chunkIndex
```

而且可以直接用 SQL 做相似度检索：

```sql
ORDER BY embedding <=> query_embedding
LIMIT 5
```

这里的意思就是：

```text
按向量距离从近到远排序，取最相似的 5 条。
```
