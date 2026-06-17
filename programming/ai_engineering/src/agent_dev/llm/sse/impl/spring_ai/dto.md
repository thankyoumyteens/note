# 请求 DTO

前端 POST SSE 请求体：

```java
package com.example.ai.dto;

/**
 * POST SSE 流式聊天请求。
 * provider 只支持 openai / deepseek / claude。
 */
public record StreamChatRequest(
        String provider,
        String system,
        String message
) {
}
```
