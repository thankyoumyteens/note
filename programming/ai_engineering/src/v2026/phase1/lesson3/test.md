# 测试流式接口

## 方式 1：curl 测试

推荐先用 curl，因为 Postman 有时会缓冲流式响应。

```bash
curl -N \
  -X POST http://localhost:8080/api/ai/chat/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"message":"请用五句话解释什么是 RAG"}'
```

关键是：

```bash
-N
```

它表示不缓冲输出。

你应该看到内容逐步出现。

---

## 方式 2：浏览器 EventSource 不适合直接测 POST

浏览器原生 `EventSource` 默认只支持 GET，不适合直接测试这个 POST 接口。

后面做前端时，可以用：

```text
fetch + ReadableStream
```

或者改成 GET SSE 接口。

目前先用 curl 测。

---

## 方式 3：Apifox / Postman

有些版本支持流式响应，但可能会缓存后一次性显示。
如果你看到最后一次性返回，不一定是后端错，优先用 curl 判断。
