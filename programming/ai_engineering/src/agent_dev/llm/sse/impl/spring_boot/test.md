# 测试

`-N` 很重要，表示关闭 curl 缓冲，否则你可能看不到实时流式输出。

```sh
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

如果测试 DeepSeek：

```sh
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

如果测试 Claude：

```sh
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
