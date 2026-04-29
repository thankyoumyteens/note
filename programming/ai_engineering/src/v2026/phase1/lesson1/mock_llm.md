# 先用 Mock LLM 跑通流程

不要一开始就接真实模型。先用 Mock 实现，确认后端结构没问题。

```java
package com.example.aigateway.client;

import org.springframework.stereotype.Component;

@Component
public class MockLlmClient implements LlmClient {

    @Override
    public String chat(String message) {
        return "这是 Mock 模型回答。你输入的是：" + message;
    }
}
```

启动项目后，用 Postman 调用：

```sh
curl --location --request POST 'http://localhost:8080/api/ai/chat' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "什么是 RAG？"
}'
```

预期返回：

```json
{
  "answer": "这是 Mock 模型回答。你输入的是：什么是 RAG？"
}
```
