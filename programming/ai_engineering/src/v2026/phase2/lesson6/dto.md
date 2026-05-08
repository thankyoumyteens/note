# 新增 DTO

## 新增请求 DTO

新建：

```text
dto/OrderAssistantRequest.java
```

```java
package com.example.aigateway.dto;

public record OrderAssistantRequest(
        String message
) {
}
```

---

## 新增响应 DTO

新建：

```text
dto/OrderAssistantResponse.java
```

```java
package com.example.aigateway.dto;

public record OrderAssistantResponse(
        String answer
) {
}
```

## 新增工具调用决策 DTO

新建：

```text
dto/ToolCallDecision.java
```

```java
package com.example.aigateway.dto;

import com.fasterxml.jackson.databind.JsonNode;

public record ToolCallDecision(
        boolean shouldCallTool,
        String toolName,
        JsonNode arguments,
        String directAnswer
) {
}
```

字段说明：

```text
shouldCallTool：是否需要调用工具
toolName：工具名称
arguments：工具参数
directAnswer：不需要工具时的直接回答
```

为什么 `arguments` 用 `JsonNode`？

因为不同工具参数结构不同。
本课只有一个工具，但后续会有多个工具，用 `JsonNode` 更灵活。

## 新增订单工具参数 DTO

新建：

```text
dto/GetOrderStatusArguments.java
```

```java
package com.example.aigateway.dto;

public record GetOrderStatusArguments(
        String orderId
) {
}
```
