# 新增 OrderAssistantService

新建：

```text
service/OrderAssistantService.java
```

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.GetOrderStatusArguments;
import com.example.aigateway.dto.ToolCallDecision;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class OrderAssistantService {

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

    public String handle(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }

        String raw = llmClient.complete(buildToolDecisionSystemPrompt(), message);
        System.out.println("LLM tool decision raw output: " + raw);

        ToolCallDecision decision = parseToolCallDecision(raw);

        if (!decision.shouldCallTool()) {
            if (decision.directAnswer() == null || decision.directAnswer().isBlank()) {
                return "我无法处理这个请求。";
            }
            return decision.directAnswer().strip();
        }

        return executeTool(decision);
    }

    private ToolCallDecision parseToolCallDecision(String raw) {
        try {
            String json = cleanupJson(raw);
            return objectMapper.readValue(json, ToolCallDecision.class);
        } catch (Exception e) {
            throw new RuntimeException("Failed to parse tool call decision. raw=" + raw, e);
        }
    }

    private String executeTool(ToolCallDecision decision) {
        if (decision.toolName() == null || decision.toolName().isBlank()) {
            throw new IllegalArgumentException("toolName cannot be empty when shouldCallTool is true");
        }

        return switch (decision.toolName()) {
            case "getOrderStatus" -> executeGetOrderStatus(decision);
            default -> throw new IllegalArgumentException("Unsupported tool: " + decision.toolName());
        };
    }

    private String executeGetOrderStatus(ToolCallDecision decision) {
        try {
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
                - 如果用户问题和订单查询无关，shouldCallTool = false，toolName = null，arguments = null，并在 directAnswer 中说明你只能处理订单状态查询
                - 如果需要调用工具，必须从用户输入中提取 orderId
                - 不要编造订单状态
                - 不要直接回答订单状态，订单状态必须通过工具查询
                """;
    }

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

注意：这里暂时复制了一份 `cleanupJson()`。
后续可以重构成公共工具类，例如：

```text
JsonOutputParser
StructuredOutputParser
```

当前先不提前重构，避免课程复杂化。
