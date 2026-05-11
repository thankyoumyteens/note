# 测试

## 先用旧实现确认项目正常

`application.yml`：

```yaml
llm:
  provider: openai-compatible
```

测试：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 Spring AI"}'
```

预期：正常返回。

---

## 切换到 Spring AI 实现

改配置：

```yaml
llm:
  provider: spring-ai
```

重启项目。

再次测试：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 Spring AI"}'
```

预期返回类似：

```json
{
  "answer": "Spring AI 是 Spring 生态中用于构建 AI 应用的框架，提供模型调用、提示词、工具调用和向量存储等抽象。"
}
```

---

## 验证日志

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

应该能看到一条：

```json
{
  "callType": "CHAT",
  "model": "spring-ai-configured-model",
  "success": true,
  "latencyMs": 1234
}
```

---

## 注意不要测 streamChat

当前 `SpringAiLlmClient.streamChat()` 暂未实现。

如果 `llm.provider=spring-ai` 时调用：

```http
POST /api/ai/chat/stream
```

会报：

```text
SpringAiLlmClient streamChat is not implemented in this lesson
```

这是预期行为。
