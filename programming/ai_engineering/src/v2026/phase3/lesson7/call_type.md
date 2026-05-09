# 给业务调用补充 callType

现在默认 `complete()` 会记录为 `COMPLETE`。

为了日志更清楚，可以改几个业务服务。

### TaskExtractionService

原来：

```java
String raw = llmClient.complete(buildExtractionSystemPrompt(), text);
```

改成：

```java
String raw = llmClient.complete(
        buildExtractionSystemPrompt(),
        text,
        LlmCallType.TASK_EXTRACTION
);
```

`repairJson` 中原来：

```java
return llmClient.complete(systemPrompt, userPrompt);
```

改成：

```java
return llmClient.complete(
        systemPrompt,
        userPrompt,
        LlmCallType.JSON_REPAIR
);
```

需要 import：

```java
import com.example.aigateway.dto.LlmCallType;
```

---

### OrderAssistantService

原来：

```java
String raw = llmClient.complete(buildToolDecisionSystemPrompt(), message);
```

改成：

```java
String raw = llmClient.complete(
        buildToolDecisionSystemPrompt(),
        message,
        LlmCallType.TOOL_DECISION
);
```

需要 import：

```java
import com.example.aigateway.dto.LlmCallType;
```
