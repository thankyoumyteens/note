# 新增调用类型枚举

新建：

```text
dto/LlmCallType.java
```

```java
package com.example.aigateway.dto;

public enum LlmCallType {
    CHAT,
    COMPLETE,
    STREAM_CHAT,
    TASK_EXTRACTION,
    JSON_REPAIR,
    TOOL_DECISION,
    UNKNOWN
}
```
