# 基于 Solon 的 Java 8 遗留系统 MCP 边车（Sidecar）改造指南

**架构背景**：

当旧版核心业务系统（Java 8 + Spring Boot 2.x）因 JDK 版本和底层框架限制，无法直接集成最新版的 Spring AI MCP SDK 时，采用 **边车模式（Sidecar）** 是最佳实践。

我们通过引入极其轻量的 **Solon** 框架，在不修改原 Spring Boot 任何代码的前提下，以独立进程启动一个占用极小、毫秒级启动的专职 MCP Server，充当大模型与遗留系统之间的跨时空桥梁。

---

### 1. 添加核心依赖

在 `pom.xml` 中引入以下依赖。请严格注意版本对齐与覆盖：

```xml
<dependency>
    <groupId>org.noear</groupId>
    <artifactId>solon-web</artifactId>
    <version>3.10.2-M2</version>
</dependency>

<dependency>
    <groupId>org.noear</groupId>
    <artifactId>solon-ai-mcp</artifactId>
    <version>3.10.2-M2</version>
</dependency>

<dependency>
    <groupId>io.projectreactor</groupId>
    <artifactId>reactor-core</artifactId>
    <version>3.4.34</version>
</dependency>

<dependency>
    <groupId>com.squareup.okhttp3</groupId>
    <artifactId>okhttp</artifactId>
    <version>3.14.9</version>
</dependency>
```

### 2. 创建 MCP Server 端点

> **⚠️ 防坑指南：**
>
> 1. 绝对不要在此类中尝试使用 `@Inject` 或 `@Autowired` 注入 Spring 的类！而是应该通过 HTTP 协议与旧系统的接口交互，保持两个容器的物理隔离。
> 2. `OkHttpClient` 和 `ObjectMapper` 必须作为全局单例（`private final`）复用，严禁在方法内部 `new`，否则会导致严重的 TCP 连接泄漏。

```java
package com.example.mcp;

import com.example.dto.Order;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.noear.solon.ai.annotation.ToolMapping;
import org.noear.solon.ai.mcp.McpChannel;
import org.noear.solon.ai.mcp.server.annotation.McpServerEndpoint;
import org.noear.solon.annotation.Param;

import java.io.IOException;

// 明确指定 channel 为 SSE，并暴露路由。默认不写会变成 stdio 导致 404！
@McpServerEndpoint(channel = McpChannel.SSE, mcpEndpoint = "/mcp/sse")
public class DemoMcpTool {

    // 最佳实践：重量级对象作为类成员单例复用
    private final OkHttpClient httpClient = new OkHttpClient();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @ToolMapping(description = "根据订单号查询公司旧版 ERP 系统的订单状态和金额")
    public String getOrderStatus(@Param(description = "订单号，例如 ORD-001") String orderId) {
        Order order = null;

        // 发起 HTTP 请求，调用本机 8080 端口上 Spring Boot 的老接口
        String url = "http://127.0.0.1:8080/demo/order?orderId=" + orderId;
        Request request = new Request.Builder().url(url).build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                // 读取 HTTP 响应体，直接反序列化为 Order 对象
                String respJson = response.body().string();
                order = objectMapper.readValue(respJson, Order.class);
                System.out.println("✅ [Solon 边车] 成功获取遗留系统数据: " + respJson);
            } else {
                System.err.println("❌ [Solon 边车] 遗留系统响应异常，状态码: " + response.code());
            }
        } catch (IOException e) {
            e.printStackTrace();
            return "网络异常，无法连接到核心业务系统：" + e.getMessage();
        }

        return order != null ? order.getOrderStatus() : "未找到该订单";
    }
}
```

### 3. 创建 Solon 应用的入口类

Solon 的容器与原项目的 Spring Boot 容器互不干扰，独立点火启动。

```java
package com.example;

import org.noear.solon.Solon;

public class McpServerApp {
    public static void main(String[] args) {
        // 🚀 启动 Solon 轻量级容器
        Solon.start(McpServerApp.class, args);
    }
}
```

### 4. 独立端口配置

在 `src/main/resources/app.yml` 中配置端口，**绝对不能与老系统的 8080 冲突**。

```yaml
server:
  port: 8081
```

### 5. 启动与日志验收

运行 `McpServerApp` 的 `main` 方法。启动速度极快（通常在 300 毫秒左右）。
启动成功后，必须在控制台确认以下两个关键信息：

1. 确认 Web 引擎已挂载：`solon.connector:main: smarthttp: Started ServerConnector@{HTTP/1.1,[http/1.1]}{http://localhost:8081}`
2. 确认频道与端点正确：`Mcp-Server started, ..., channel=sse, sseEndpoint=/mcp/sse, messageEndpoint=/mcp/sse/message, ...`

### 6. 连通大模型客户端 (Python LangGraph)

在 Python 端，配置 `MultiServerMCPClient` 指向这个刚刚启动的 Solon 边车节点：

```python
client = MultiServerMCPClient({
    "java_erp_microservice": {
        # 直接敲门访问 Solon 的 8081 端口
        "url": "http://127.0.0.1:8081/mcp/sse",
        "transport": "sse",
    }
})
```
