# 这一课真正要理解的点

## 1. 流式输出不是普通 JSON

普通接口返回：

```json
{
  "answer": "完整回答"
}
```

流式接口返回：

```text
data: 第一段

data: 第二段

data: 第三段
```

所以前端处理方式完全不同。

---

## 2. 后端返回的是 Flux

```java
Flux<String>
```

它代表多个异步片段。

你可以理解为：

```text
String：一个完整结果
Flux<String>：一串不断到来的结果
```

---

## 3. 模型供应商返回的是 chunk

每个 chunk 不是完整回答，而是增量：

```json
{
  "choices": [
    {
      "delta": {
        "content": "RAG"
      }
    }
  ]
}
```

所以后端要把很多个 `delta.content` 拼起来，前端最终看到完整答案。
