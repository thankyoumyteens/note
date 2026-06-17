# 测试

## OpenAI

```bash
curl -N \
  -X POST "http://localhost:8080/api/ai/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "provider": "openai",
    "system": "你是一个严谨的 Java 后端助手。",
    "message": "用三句话解释 RAG"
  }'
```

## DeepSeek

```bash
curl -N \
  -X POST "http://localhost:8080/api/ai/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "provider": "deepseek",
    "system": "你是一个严谨的 Java 后端助手。",
    "message": "解释一下 WebClient 和 RestClient 的区别"
  }'
```

## Claude

```bash
curl -N \
  -X POST "http://localhost:8080/api/ai/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "provider": "claude",
    "system": "You are a helpful Java backend assistant.",
    "message": "Explain Server-Sent Events in simple terms."
  }'
```
