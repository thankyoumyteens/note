# 新增 CheckOrderToolExecutor

把第 16 课写死在 `AgentStepExecutor` 里的模拟订单检查，迁移成标准工具。

工具应该同时包含：

```text
工具定义
参数要求
执行逻辑
错误返回
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/executor/CheckOrderToolExecutor.java
```

```java
package com.example.aigateway.tool.executor;

import com.example.aigateway.tool.dto.ToolDefinition;
import com.example.aigateway.tool.dto.ToolParameterDefinition;
import com.example.aigateway.tool.dto.ToolRequest;
import com.example.aigateway.tool.dto.ToolResult;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;

/**
 * 检查订单工具。
 *
 * 第 17 课仍然使用模拟数据。
 * 第 18 课 MCP 之后，可以把真实企业系统封装为 MCP Tool。
 */
@Component
public class CheckOrderToolExecutor implements ToolExecutor {

    public static final String TOOL_NAME = "checkOrder";

    @Override
    public ToolDefinition definition() {
        return new ToolDefinition(
                TOOL_NAME,
                "根据 orderId 查询订单退款状态、退款风险和处理建议。适用于退款进度、订单状态、重复退款风险等问题。",
                List.of(
                        new ToolParameterDefinition(
                                "orderId",
                                "string",
                                true,
                                "订单编号，例如 ORDER-1001"
                        )
                ),
                List.of("employee", "finance", "support"),
                false
        );
    }

    @Override
    public ToolResult execute(ToolRequest request) {
        Object orderIdValue = request.arguments().get("orderId");

        if (orderIdValue == null || orderIdValue.toString().isBlank()) {
            return ToolResult.failure(
                    TOOL_NAME,
                    "MISSING_ARGUMENT",
                    "orderId is required"
            );
        }

        String orderId = orderIdValue.toString();

        if (!"ORDER-1001".equals(orderId)) {
            return ToolResult.failure(
                    TOOL_NAME,
                    "ORDER_NOT_FOUND",
                    "order not found: " + orderId
            );
        }

        return ToolResult.success(
                TOOL_NAME,
                Map.of(
                        "orderId", "ORDER-1001",
                        "status", "REFUND_REQUESTED",
                        "refundStatus", "PENDING_REVIEW",
                        "risk", "POSSIBLE_DUPLICATE_REFUND",
                        "message", "订单存在退款申请，但需要人工确认是否重复退款。"
                )
        );
    }
}
```

### 代码说明

`description` 很重要。后续让 LLM 选择工具时，模型主要就是看工具描述和参数定义。
