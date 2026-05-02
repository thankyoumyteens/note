# 测试接口

启动项目。

调用：

```sh
curl --location --request POST 'http://localhost:8080/api/ai/chat' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "请用三句话解释什么是 RAG。"
}'
```

预期返回类似：

```json
{
  "answer": "RAG 是检索增强生成..."
}
```
