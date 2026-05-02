# 新增 DTO

## 1. 请求 DTO

新建：

```text
dto/TaskExtractionRequest.java
```

代码：

```java
package com.example.aigateway.dto;

public record TaskExtractionRequest(
        String text
) {
}
```

---

## 2. 优先级枚举

新建：

```text
dto/TaskPriority.java
```

代码：

```java
package com.example.aigateway.dto;

public enum TaskPriority {
    LOW,
    MEDIUM,
    HIGH,
    UNKNOWN
}
```

---

## 3. 响应 DTO

新建：

```text
dto/TaskExtractionResult.java
```

代码：

```java
package com.example.aigateway.dto;

public record TaskExtractionResult(
        String taskName,
        String dueTimeText,
        TaskPriority priority,
        String assignee
) {
}
```

先用 `dueTimeText`，不要急着转 `LocalDateTime`。
因为“明天下午三点”这种相对时间需要结合用户时区和当前日期，后面单独做时间标准化。
