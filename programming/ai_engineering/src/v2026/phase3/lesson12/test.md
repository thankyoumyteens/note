# 测试方式

### 启动 PostgreSQL + pgvector

```bash
docker start ai-gateway-pgvector
```

确认 pgvector 可用：

```bash
docker exec -it ai-gateway-pgvector psql -U ai -d ai_gateway -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

---

### 启动 Java 服务

```bash
mvn spring-boot:run
```

如果启动时报 `VectorStore` bean 不存在，优先检查：

```text
Spring AI pgvector 依赖是否正确
spring.ai.vectorstore.pgvector 配置是否生效
EmbeddingModel 是否存在
```

---

### 准备测试文档

```bash
cat > spring-ai-rag-test.txt <<'EOF'
Spring AI 是 Spring 生态中的 AI 应用开发框架。
它提供 ChatModel、EmbeddingModel、VectorStore 等抽象。
VectorStore 可以屏蔽不同向量数据库的差异。
在企业项目中，Spring AI 可以作为生态适配层，但不应该替代业务自己的架构边界。
EOF
```

---

### 上传到 Spring AI RAG Demo

```bash
curl -X POST http://localhost:8080/api/spring-ai/rag/documents \
  -F "file=@spring-ai-rag-test.txt"
```

预期：

```json
{
  "documentCount": 1
}
```

---

### 查询 Spring AI RAG Demo

```bash
curl -X POST http://localhost:8080/api/spring-ai/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"Spring AI 的 VectorStore 有什么作用？","topK":3}'
```

预期：

```json
{
  "answer": "...VectorStore 可以屏蔽不同向量数据库的差异...",
  "documents": [
    {
      "text": "...",
      "metadata": {
        "filename": "spring-ai-rag-test.txt",
        "source": "spring-ai-rag-demo"
      }
    }
  ]
}
```

---

### 对比第 11 课接口

第 11 课手写 RAG：

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"RAG 的核心思想是什么？","topK":3}'
```

第 12 课 Spring AI RAG：

```bash
curl -X POST http://localhost:8080/api/spring-ai/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"Spring AI 的 VectorStore 有什么作用？","topK":3}'
```

你要能解释：

```text
/api/rag/query 是手写主线 RAG。
/api/spring-ai/rag/query 是 Spring AI 框架适配 Demo。
```
