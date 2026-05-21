# 新增 DTO

## 新增请求 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/OrderAssistantRequest.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 订单助手请求 DTO。
 *
 * message 表示用户输入的自然语言请求。
 */
public record OrderAssistantRequest(
        String message
) {
}
```

---

## 新增响应 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/OrderAssistantResponse.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 订单助手响应 DTO。
 *
 * answer 是最终返回给用户看的文本。
 */
public record OrderAssistantResponse(
        String answer
) {
}
```

## 新增工具调用决策 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/ToolCallDecision.java
```

代码：

```java
package com.example.aigateway.dto;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * 工具调用决策 DTO。
 *
 * 模型不会真正执行工具。
 * 模型只负责输出这个结构，告诉 Java 后端：
 * - 是否需要调用工具
 * - 要调用哪个工具
 * - 工具参数是什么
 * - 如果不需要工具，直接回答什么
 */
public record ToolCallDecision(
        boolean shouldCallTool,
        String toolName,
        JsonNode arguments,
        String directAnswer
) {
}
```

为什么 `arguments` 用 `JsonNode`：

```text
不同工具参数结构不同。
当前只有 getOrderStatus，后续可能有 searchKnowledgeBase、createTicket 等工具。
JsonNode 可以先承载任意工具参数，再按 toolName 映射成具体 DTO。
```

## 新增订单工具参数 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/GetOrderStatusArguments.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * getOrderStatus 工具参数 DTO。
 *
 * orderId 是订单号。
 */
public record GetOrderStatusArguments(
        String orderId
) {
}
```
