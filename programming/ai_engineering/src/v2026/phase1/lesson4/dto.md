# 新增 DTO

## 1. 请求 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/TaskExtractionRequest.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 任务抽取请求 DTO。
 *
 * text 表示用户输入的一段自然语言任务描述。
 */
public record TaskExtractionRequest(
        String text
) {
}
```

---

## 2. 优先级枚举

文件：

```text
src/main/java/com/example/aigateway/dto/TaskPriority.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 任务优先级枚举。
 *
 * 使用 enum 而不是 String，可以限制模型输出最终只能映射到固定值。
 */
public enum TaskPriority {

    /**
     * 低优先级。
     */
    LOW,

    /**
     * 中优先级。
     */
    MEDIUM,

    /**
     * 高优先级。
     */
    HIGH,

    /**
     * 无法判断优先级。
     */
    UNKNOWN
}
```

---

## 3. 响应 DTO

文件：

```text
src/main/java/com/example/aigateway/dto/TaskExtractionResult.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 任务抽取结果 DTO。
 *
 * 这是 Java 后端最终希望消费的结构化结果。
 */
public record TaskExtractionResult(
        String taskName,
        String dueTimeText,
        TaskPriority priority,
        String assignee
) {
}
```

字段含义：

```text
taskName：任务名称
dueTimeText：原文中的时间表达
priority：优先级
assignee：负责人
```
