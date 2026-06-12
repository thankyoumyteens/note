# 新增 MCP JSON-RPC DTO

MCP 底层是基于 JSON-RPC 风格的方法调用，本课先定义最小请求/响应结构。

你不需要先完全手写整个 MCP specification。第 18 课只做最小集成闭环：

```text
tools/list
tools/call
resources/list
prompts/list
```

### 代码

目录：

```text
src/main/java/com/example/aigateway/mcp/dto/
```

`McpJsonRpcRequest.java`

```java
package com.example.aigateway.mcp.dto;

import java.util.Map;

/**
 * 最小 JSON-RPC 请求。
 */
public record McpJsonRpcRequest(
        String jsonrpc,
        String id,
        String method,
        Map<String, Object> params
) {
    public static McpJsonRpcRequest of(String id, String method, Map<String, Object> params) {
        return new McpJsonRpcRequest(
                "2.0",
                id,
                method,
                params == null ? Map.of() : params
        );
    }
}
```

`McpJsonRpcResponse.java`

```java
package com.example.aigateway.mcp.dto;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * 最小 JSON-RPC 响应。
 *
 * result / error 暂时用 JsonNode 保存，避免过早绑定完整 MCP schema。
 */
public record McpJsonRpcResponse(
        String jsonrpc,
        String id,
        JsonNode result,
        JsonNode error
) {
    public boolean success() {
        return error == null || error.isNull();
    }
}
```

### 代码说明

`result` 用 `JsonNode`，是为了先跑通协议，不一开始就把所有 MCP schema 全部建模。
