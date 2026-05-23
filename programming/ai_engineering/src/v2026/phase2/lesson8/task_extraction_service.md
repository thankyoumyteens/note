# 修改 TaskExtractionService 的 callType

把任务抽取调用改成：

```java
String rawOutput = llmClient.complete(
        buildExtractionSystemPrompt(),
        text,
        LlmCallType.TASK_EXTRACTION
);
```

把 JSON 修复调用改成：

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
