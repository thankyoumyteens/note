# 新增 McpProperties

把 MCP server 配置放到 `application.yml` 中，避免写死。

企业系统里不会只有一个 MCP server。可能会有：

```text
order-mcp-server
crm-mcp-server
ticket-mcp-server
finance-mcp-server
```

第 18 课先配置一个 HTTP JSON-RPC 风格的 MCP server。

### 代码

文件：

```text
src/main/java/com/example/aigateway/mcp/config/McpServerProperties.java
```

```java
package com.example.aigateway.mcp.config;

/**
 * 单个 MCP Server 配置。
 *
 * 第 18 课先使用 HTTP JSON-RPC 风格。
 * 后续可扩展 STDIO / SSE / streamable HTTP 等 transport。
 */
public class McpServerProperties {

    /**
     * MCP Server 名称，例如 order。
     */
    private String name;

    /**
     * MCP Server endpoint，例如 http://localhost:9001/mcp。
     */
    private String endpoint;

    /**
     * 是否启用。
     */
    private boolean enabled = true;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
}
```

文件：

```text
src/main/java/com/example/aigateway/mcp/config/McpProperties.java
```

```java
package com.example.aigateway.mcp.config;

import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * MCP 配置。
 */
@ConfigurationProperties(prefix = "ai.mcp")
public class McpProperties {

    private List<McpServerProperties> servers = new ArrayList<>();

    public List<McpServerProperties> getServers() {
        return servers;
    }

    public void setServers(List<McpServerProperties> servers) {
        this.servers = servers;
    }
}
```

`application.yml`：

```yaml
ai:
  mcp:
    servers:
      - name: order
        endpoint: http://localhost:9001/mcp
        enabled: true
```

启动类启用：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class,
        RagProperties.class,
        ContextProperties.class,
        AgentProperties.class,
        ToolProperties.class,
        McpProperties.class
})
```

### 代码说明

当前先只做 HTTP endpoint 配置。STDIO MCP server 会涉及本地进程启动、命令白名单和安全隔离，本课暂不展开。
