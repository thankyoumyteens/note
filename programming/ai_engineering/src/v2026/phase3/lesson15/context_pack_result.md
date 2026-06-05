# 新增 ContextBudget 和 ContextPackResult

定义上下文打包结果。

Context packing 不是简单拼字符串，而是要返回：

```text
最终保留了哪些 context
丢弃了哪些 context
总 token 多少
是否发生截断
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/dto/ContextBudget.java
```

```java
package com.example.aigateway.context.dto;

/**
 * 上下文预算。
 */
public record ContextBudget(
        int maxInputTokens,
        int reservedOutputTokens,
        int maxContextTokens
) {
}
```

文件：

```text
src/main/java/com/example/aigateway/context/dto/ContextPackResult.java
```

```java
package com.example.aigateway.context.dto;

import java.util.List;

/**
 * 上下文打包结果。
 */
public record ContextPackResult(
        List<ContextItem> selectedItems,
        List<ContextItem> droppedItems,
        int totalTokens,
        boolean truncated
) {
}
```

### 代码说明

`truncated = true` 表示上下文发生了裁剪。

这在调试 RAG 和 Agent 时很重要。
