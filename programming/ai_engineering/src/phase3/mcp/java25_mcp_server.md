# 把 Java 25 项目改造成 MCP Server

### 1. 添加依赖

```groovy
repositories {
    mavenCentral()
    // 添加 Spring 官方的 Milestone 仓库！
    maven { url 'https://repo.spring.io/milestone' }
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'

    // 引入 Spring AI
    implementation platform("org.springframework.ai:spring-ai-bom:2.0.0-M4")
    implementation 'org.springframework.ai:spring-ai-starter-mcp-server-webmvc'

    // ...
}
```

### 2. 配置文件

```yaml
server:
  port: 8080

spring:
  ai:
    mcp:
      server:
        # Tomcat 的 SSE 模式又 BUG
        # 废弃传统的 SSE 模式，使用专为 WebMVC 打造的全新 STREAMABLE 协议引擎
        protocol: STREAMABLE
```

### 3. OrderMcpService.java

```java
package com.example.demo.mcp;

import com.example.demo.model.OrderDto;
import com.example.demo.service.OrderBusinessService;
import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.stereotype.Service;

@Service
public class OrderMcpService {

    // 🌟 使用 private final 声明你的底层业务 Service
    private final OrderBusinessService orderBusinessService;

    // 🌟 通过构造器注入（Spring 会自动感知并传入）
    public OrderMcpService(OrderBusinessService orderBusinessService) {
        this.orderBusinessService = orderBusinessService;
    }

    // 🌟 给大模型提供的工具
    @McpTool(description = "根据订单号查询旧版ERP系统的订单状态和金额")
    public OrderDto getOrderStatus(String orderId) {

        System.out.println("🚀 [原生 MCP 节点] 收到大模型指令，查询订单: " + orderId);

        // 🌟 直接调用你注入的 service 方法
        // 你的底层查库、缓存、微服务调用全在 OrderBusinessService 里，这里只负责转接。
        return orderBusinessService.findOrderDetails(orderId);
    }
}
```

### 4. 连通大模型客户端 (Python LangGraph)

```py
client = MultiServerMCPClient({
    "java_erp_microservice": {
        "url": "http://127.0.0.1:8080/mcp",  # 指向你的 Spring Boot 容器
        "transport": "http",  # 切换为 http 协议
    }
})
```
