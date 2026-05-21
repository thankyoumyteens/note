# 新增 OrderAssistantService

文件：

```text
src/main/java/com/example/aigateway/service/OrderAssistantService.java
```

代码：

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.GetOrderStatusArguments;
import com.example.aigateway.dto.ToolCallDecision;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

/**
 * 订单助手服务。
 *
 * 职责：
 * 1. 让模型判断是否需要调用订单工具
 * 2. 解析模型输出的工具调用决策
 * 3. 校验工具名称白名单
 * 4. 校验工具参数
 * 5. 执行 Java 后端工具
 */
@Service
public class OrderAssistantService {

    private static final String TOOL_GET_ORDER_STATUS = "getOrderStatus";

    private final LlmClient llmClient;
    private final ObjectMapper objectMapper;
    private final OrderToolService orderToolService;

    public OrderAssistantService(
            LlmClient llmClient,
            ObjectMapper objectMapper,
            OrderToolService orderToolService
    ) {
        this.llmClient = llmClient;
        this.objectMapper = objectMapper;
        this.orderToolService = orderToolService;
    }

    /**
     * 处理用户订单助手请求。
     */
    public String handle(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }

        String rawOutput = llmClient.complete(
                buildToolDecisionSystemPrompt(),
                message
        );

        System.out.println("LLM tool decision raw output: " + rawOutput);

        ToolCallDecision decision = parseToolCallDecision(rawOutput);

        if (!decision.shouldCallTool()) {
            return handleDirectAnswer(decision);
        }

        return executeTool(decision);
    }

    /**
     * 解析模型输出的工具调用决策。
     *
     * 本课做基础 JSON 清理和解析。
     * 第 7 课会对工具选择准确率做 eval。
     */
    private ToolCallDecision parseToolCallDecision(String rawOutput) {
        try {
            String json = cleanupJson(rawOutput);

            return objectMapper.readValue(
                    json,
                    ToolCallDecision.class
            );

        } catch (Exception e) {
            throw new RuntimeException(
                    "Failed to parse tool call decision. rawOutput=" + rawOutput,
                    e
            );
        }
    }

    /**
     * 不需要调用工具时，直接返回模型给出的 directAnswer。
     */
    private String handleDirectAnswer(ToolCallDecision decision) {
        if (decision.directAnswer() == null || decision.directAnswer().isBlank()) {
            return "我只能处理订单状态查询相关请求。";
        }

        return decision.directAnswer().strip();
    }

    /**
     * 执行工具。
     *
     * 这里必须使用白名单。
     * 不能根据模型返回的 toolName 任意反射调用 Java 方法。
     */
    private String executeTool(ToolCallDecision decision) {
        if (decision.toolName() == null || decision.toolName().isBlank()) {
            throw new IllegalArgumentException("toolName cannot be empty when shouldCallTool is true");
        }

        return switch (decision.toolName()) {
            case TOOL_GET_ORDER_STATUS -> executeGetOrderStatus(decision);
            default -> throw new IllegalArgumentException("Unsupported tool: " + decision.toolName());
        };
    }

    /**
     * 执行 getOrderStatus 工具。
     */
    private String executeGetOrderStatus(ToolCallDecision decision) {
        try {
            if (decision.arguments() == null || decision.arguments().isNull()) {
                throw new IllegalArgumentException("arguments cannot be empty");
            }

            GetOrderStatusArguments arguments = objectMapper.treeToValue(
                    decision.arguments(),
                    GetOrderStatusArguments.class
            );

            if (arguments.orderId() == null || arguments.orderId().isBlank()) {
                throw new IllegalArgumentException("orderId cannot be empty");
            }

            return orderToolService.getOrderStatus(arguments.orderId());

        } catch (Exception e) {
            throw new RuntimeException("Failed to execute getOrderStatus tool", e);
        }
    }

    /**
     * 构造工具调用决策 Prompt。
     *
     * 注意：
     * 模型只能输出工具调用决策 JSON。
     * 订单状态不能由模型编造，必须通过 Java 后端工具查询。
     */
    private String buildToolDecisionSystemPrompt() {
        return """
                你是一个订单助手的工具调用决策器。

                你需要判断用户请求是否需要调用后端工具。

                当前可用工具：

                1. getOrderStatus
                描述：根据订单号查询订单状态。
                参数：
                {
                  "orderId": "订单号，字符串"
                }

                你只能输出 JSON，不能输出 Markdown，不能输出解释，不能使用 ```json 代码块。

                输出 JSON 格式：
                {
                  "shouldCallTool": true 或 false,
                  "toolName": "getOrderStatus 或 null",
                  "arguments": {
                    "orderId": "订单号"
                  },
                  "directAnswer": "如果不需要调用工具，则直接回答；如果需要调用工具，则为 null"
                }

                判断规则：
                - 如果用户想查询订单状态、物流状态、订单进度，shouldCallTool = true，toolName = "getOrderStatus"
                - 如果用户问题和订单查询无关，shouldCallTool = false，toolName = null，arguments = null
                - 如果不需要调用工具，请在 directAnswer 中说明你只能处理订单状态查询
                - 如果需要调用工具，必须从用户输入中提取 orderId
                - 不要编造订单状态
                - 不要直接回答订单状态，订单状态必须通过工具查询
                """;
    }

    /**
     * 基础 JSON 清理。
     *
     * 复用前面结构化输出课程的思想：
     * - 去掉 Markdown 代码块
     * - 从文本中提取第一个 { 到最后一个 }
     */
    private String cleanupJson(String raw) {
        if (raw == null) {
            throw new IllegalStateException("LLM output is null");
        }

        String text = raw.strip();

        if (text.startsWith("```json")) {
            text = text.substring("```json".length()).strip();
        }

        if (text.startsWith("```")) {
            text = text.substring("```".length()).strip();
        }

        if (text.endsWith("```")) {
            text = text.substring(0, text.length() - 3).strip();
        }

        int firstBrace = text.indexOf('{');
        int lastBrace = text.lastIndexOf('}');

        if (firstBrace >= 0 && lastBrace > firstBrace) {
            text = text.substring(firstBrace, lastBrace + 1).strip();
        }

        return text;
    }
}
````

## 什么是工具白名单

模型输出的 `toolName` 不能直接相信。

它可能输出：

```json
{
  "toolName": "deleteAllOrders",
  "arguments": {}
}
```

如果后端根据模型返回的名字直接反射调用方法，会非常危险。

所以后端必须做白名单：

```java
switch (toolName) {
    case "getOrderStatus" -> executeGetOrderStatus(...);
    default -> reject;
}
```

当前系统只允许：

```text
getOrderStatus
```

其他工具名全部拒绝。
