# 测试方式

### 启动服务

```bash
mvn spring-boot:run
```

预期：服务正常启动，JPA 自动创建表。

---

### 测试 requestId / traceId 响应头

```bash
curl -i -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

预期响应头包含：

```text
X-Request-Id: ...
X-Trace-Id: ...
```

---

### 查询模型调用日志

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

预期：返回数据库中的最近 100 条模型调用日志。

---

### 按 callType 查询

```bash
curl "http://localhost:8080/api/ai/llm-call-logs?callType=CHAT"
```

预期：只返回 `CHAT` 类型调用日志。

---

### 查询基础统计

```bash
curl http://localhost:8080/api/ai/llm-call-stats
```

预期类似：

```json
{
  "total": 5,
  "success": 5,
  "failure": 0,
  "avgLatencyMs": 1320.4,
  "totalTokens": 862
}
```

---

### 测试工具调用日志

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"帮我查一下订单 10086 的状态"}'
```

然后查询：

```bash
curl http://localhost:8080/api/ai/tool-call-logs
```

预期：能看到 `getOrderStatus` 的工具调用日志。

---

### 用 traceId 串联查询

从模型调用日志里拿到一个 `traceId`，然后查：

```bash
curl "http://localhost:8080/api/ai/llm-call-logs?traceId=你的traceId"
curl "http://localhost:8080/api/ai/tool-call-logs?traceId=你的traceId"
```

预期：可以看到同一次请求相关的模型调用日志和工具调用日志。

---

### 打开 H2 Console

访问：

```text
http://localhost:8080/h2-console
```

使用：

```text
JDBC URL: jdbc:h2:mem:ai_gateway
User Name: sa
Password: 留空
```

查看表：

```sql
SELECT * FROM LLM_CALL_LOGS;
SELECT * FROM TOOL_CALL_LOGS;
```
