# 测试方式

### 测试当前 provider

先设置：

```yaml
llm:
  provider: spring-ai
```

启动：

```bash
mvn spring-boot:run
```

预期：项目正常启动，且没有 `LlmClient` Bean 冲突。

---

### 5.2 测试普通聊天

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

预期：返回真实模型回答。

---

### 测试结构化输出仍可用

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"明天下午三点提醒我给张三发报价单，优先级高。"}'
```

预期：仍能返回 `TaskExtractionResult`。

这一步重点是确认：

```text
TaskExtractionService 没有直接依赖 Spring AI
```

---

### 测试工具调用仍可用

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"帮我查一下订单 10086 的状态"}'
```

预期：仍然返回订单状态。

这一步重点是确认：

```text
OrderAssistantService 没有直接依赖 Spring AI
```

---

### 测试日志仍可用

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

预期：可以看到 `SpringAiLlmClient` 产生的模型调用日志。

---

### 切回手写 Client

把配置改回：

```yaml
llm:
  provider: openai-compatible
```

重启后再次调用：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"hello"}'
```

预期：接口仍正常。
