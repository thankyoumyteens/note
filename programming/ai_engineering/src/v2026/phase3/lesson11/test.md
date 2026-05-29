# 测试方式

### 启动 pgvector

```bash
docker start ai-gateway-pgvector
```

如果还没有创建：

```bash
docker run --name ai-gateway-pgvector \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai123456 \
  -e POSTGRES_DB=ai_gateway \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
```

---

### 启动 Java 服务

```bash
mvn spring-boot:run
```

预期：

```text
服务启动成功
schema.sql 自动执行
rag_documents / rag_chunks 表存在
```

---

### 准备测试文档

创建文件：

```bash
cat > rag-test.txt <<'EOF'
RAG 是 Retrieval-Augmented Generation 的缩写，中文通常叫检索增强生成。
它的核心思想是在大语言模型回答前，先从外部知识库中检索相关内容。
RAG 可以降低模型幻觉，并让模型回答包含私有知识或最新知识的问题。
一个基础 RAG 系统通常包括文档解析、文本切分、embedding、向量检索和答案生成。
EOF
```

---

### 上传文档

```bash
curl -X POST http://localhost:8080/api/rag/documents \
  -F "file=@rag-test.txt"
```

预期类似：

```json
{
  "documentId": "....",
  "filename": "rag-test.txt",
  "chunkCount": 1
}
```

---

### 查询 RAG

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"RAG 的核心思想是什么？","topK":3}'
```

预期：

```json
{
  "answer": "RAG 的核心思想是在大语言模型回答前，先从外部知识库中检索相关内容。",
  "chunks": [
    {
      "documentId": "...",
      "chunkIndex": 0,
      "content": "...",
      "score": 0.8
    }
  ]
}
```

---

### 测试无法回答的问题

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"这个文档有没有提到 Kubernetes？","topK":3}'
```

理想回答：

```text
根据已提供文档无法确定。
```

如果模型仍然编造答案，说明 prompt 约束还不够强。这个问题放到第 13 课 RAG 质量增强处理。
