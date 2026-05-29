# 启动 PostgreSQL + pgvector

RAG 需要存储向量，并根据问题向量检索最相似的 chunk。普通 PostgreSQL 不支持向量相似度检索，所以这里使用 `pgvector` 扩展。

RAG 的检索阶段不是 SQL 关键词匹配，而是：

```text
问题文本 -> embedding 向量
文档 chunk -> embedding 向量
计算两个向量的相似度
取 top-k 最相似 chunk
```

本课用 pgvector 做最小向量数据库。

启动数据库：

```bash
docker run --name ai-gateway-pgvector \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai123456 \
  -e POSTGRES_DB=ai_gateway \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

如果容器已存在：

```bash
docker start ai-gateway-pgvector
```
