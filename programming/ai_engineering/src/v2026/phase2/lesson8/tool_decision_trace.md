# 修改 OrderAssistantService 记录 Tool Decision Trace

## 什么是 Tool Decision Trace

第 7 课的订单助手 eval 是黑盒评估：

```text
输入 -> /api/ai/order-assistant -> 看最终 answer 是否包含预期文本
```

但它看不到模型内部是否正确选择了工具。

更理想的是记录：

```text
shouldCallTool
toolName
arguments.orderId
toolResult
toolLatencyMs
toolSuccess
toolErrorMessage
```

这就是 **Tool Decision Trace**。

它的作用：

```text
让 eval 从“只看最终回答”升级为“同时看内部工具决策”
```

## 代码实现

给 `OrderAssistantService` 注入：

```java
private final ToolCallLogService toolCallLogService;
```

构造器增加：

```java
ToolCallLogService toolCallLogService
```

并赋值：

```java
this.toolCallLogService = toolCallLogService;
```

需要 import：

```java
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.dto.ToolCallLog;
import com.example.aigateway.service.ToolCallLogService;
```

把 `handle` 方法改成这个结构：

```java
public String handle(String message) {
    if (message == null || message.isBlank()) {
        throw new IllegalArgumentException("message cannot be empty");
    }

    long start = System.currentTimeMillis();

    ToolCallDecision decision = null;

    try {
        String rawOutput = llmClient.complete(
                buildToolDecisionSystemPrompt(),
                message,
                LlmCallType.TOOL_DECISION
        );

        System.out.println("LLM tool decision raw output: " + rawOutput);

        decision = parseToolCallDecision(rawOutput);

        String result;

        if (!decision.shouldCallTool()) {
            result = handleDirectAnswer(decision);

            recordToolCallLog(
                    decision,
                    result,
                    true,
                    System.currentTimeMillis() - start,
                    null
            );

            return result;
        }

        result = executeTool(decision);

        recordToolCallLog(
                decision,
                result,
                true,
                System.currentTimeMillis() - start,
                null
        );

        return result;

    } catch (Exception e) {
        recordToolCallLog(
                decision,
                null,
                false,
                System.currentTimeMillis() - start,
                e.getMessage()
        );

        throw e;
    }
}
```

新增辅助方法：

```java
private void recordToolCallLog(
        ToolCallDecision decision,
        String toolResult,
        boolean success,
        long latencyMs,
        String errorMessage
) {
    try {
        boolean shouldCallTool = decision != null && decision.shouldCallTool();
        String toolName = decision == null ? null : decision.toolName();
        String argumentsJson = decision == null || decision.arguments() == null
                ? null
                : decision.arguments().toString();

        toolCallLogService.record(ToolCallLog.of(
                shouldCallTool,
                toolName,
                argumentsJson,
                toolResult,
                success,
                latencyMs,
                errorMessage
        ));
    } catch (Exception logError) {
        // 日志记录失败不能影响主业务流程。
        System.err.println("Failed to record tool call log: " + logError.getMessage());
    }
}
```
