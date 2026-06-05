# 新增 ContextItemType 和 ContextItem

把不同来源的上下文统一成一个结构。

上下文来源很多：

```text
RAG chunk
tool result
conversation history
user instruction
system instruction
memory
```

如果每种来源都自己拼 prompt，后面会失控。

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/dto/ContextItemType.java
```

```java
package com.example.aigateway.context.dto;

/**
 * 上下文片段类型。
 */
public enum ContextItemType {
    RAG_CHUNK,
    TOOL_RESULT,
    CONVERSATION_HISTORY,
    MEMORY,
    SYSTEM_INSTRUCTION,
    USER_QUERY
}
```

文件：

```text
src/main/java/com/example/aigateway/context/dto/ContextItem.java
```

```java
package com.example.aigateway.context.dto;

import java.util.Map;

/**
 * 一个可放入 prompt 的上下文片段。
 *
 * priority 越大，越优先保留。
 * tokenCount 由 TokenEstimator 估算。
 */
public record ContextItem(
        ContextItemType type,
        String content,
        int priority,
        int tokenCount,
        Map<String, Object> metadata
) {
}
```

### 代码说明

`priority` 用来决定超预算时先保留谁。

例如：

```text
用户问题：priority = 100
高分 RAG chunk：priority = 80
低分 RAG chunk：priority = 40
旧对话历史：priority = 20
```
