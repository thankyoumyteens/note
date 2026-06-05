# 测试方式

### 测试 TokenEstimator

可以临时写一个测试接口或单元测试。

最简单单元测试：

```java
@Test
void estimateChineseText() {
    TokenEstimator estimator = new TokenEstimator();
    int tokens = estimator.estimate("RAG 可以降低模型幻觉");
    assertTrue(tokens > 0);
}
```

### 测试 RAG 查询仍可用

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-finance-001" \
  -H "X-Roles: finance" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销需要多少天内提交？","topK":5}'
```

预期：

```text
仍能回答
仍返回 chunks
权限隔离仍生效
```

### 测试超预算裁剪

临时把配置改小：

```yaml
ai:
  context:
    max-rag-context-tokens: 100
    max-chunk-tokens: 50
```

再查询：

```bash
curl -X POST http://localhost:8080/api/rag/query \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-finance-001" \
  -H "X-Roles: finance" \
  -H "Content-Type: application/json" \
  --data-raw '{"question":"报销规则是什么？","topK":10}'
```

预期：

```text
系统仍能回答
日志或 prompt 中可以看到 truncated=true
部分 context 被 dropped
```

测试完把配置恢复。
