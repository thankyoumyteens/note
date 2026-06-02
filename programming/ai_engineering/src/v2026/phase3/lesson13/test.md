# 测试方式

### 启动 Java 服务

```bash
mvn spring-boot:run
```

---

### 确认已有 RAG 测试文档

如果没有，先上传：

```bash
cat > rag-test.txt <<'EOF'
RAG 是 Retrieval-Augmented Generation 的缩写，中文通常叫检索增强生成。
它的核心思想是在大语言模型回答前，先从外部知识库中检索相关内容。
RAG 可以降低模型幻觉，并让模型回答包含私有知识或最新知识的问题。
一个基础 RAG 系统通常包括文档解析、文本切分、embedding、向量检索和答案生成。
EOF

curl -X POST http://localhost:8080/api/rag/documents \
  -F "file=@rag-test.txt"
```

---

### 测试正常回答

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"RAG 的核心思想是什么？","topK":3}'
```

预期：

```text
answer 中回答 RAG 的核心思想
chunks 不为空
rewrittenQuestion 有值
hasEnoughContext = true
```

---

### 测试 no-answer

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"这个文档有没有提到 Kubernetes？","topK":3}'
```

理想预期：

```json
{
  "answer": "根据已提供文档无法确定。",
  "hasEnoughContext": false
}
```

如果没有触发 no-answer，可以调高：

```yaml
ai:
  rag:
    min-context-score: 0.4
```

---

### 测试 citation

看回答中是否出现：

```text
[1]
[2]
```

并确认响应里的 chunks 有：

```json
"citationId": 1
```

---

### 运行 RAG eval

```bash
cd python-tools
uv run python scripts/eval_rag_basic.py
```

预期看到：

```text
=== RAG Eval Result ===
total: 3
passed: ...
failed: ...
pass_rate: ...
```
