# 新增订单工具 Service

文件：

```text
src/main/java/com/example/aigateway/service/OrderToolService.java
```

代码：

```java
package com.example.aigateway.service;

import org.springframework.stereotype.Service;

/**
 * 订单工具服务。
 *
 * 当前使用 Mock 数据模拟订单系统。
 * 后续真实项目中，这里可以调用：
 * - 订单数据库
 * - 订单微服务
 * - ERP 系统
 * - 第三方电商平台 API
 */
@Service
public class OrderToolService {

    /**
     * 根据订单号查询订单状态。
     *
     * 这是一个只读工具，不修改业务数据。
     */
    public String getOrderStatus(String orderId) {
        if (orderId == null || orderId.isBlank()) {
            throw new IllegalArgumentException("orderId cannot be empty");
        }

        String normalizedOrderId = orderId.strip();

        return switch (normalizedOrderId) {
            case "10086" -> "订单 10086 当前状态是：已发货，预计明天送达。";
            case "10010" -> "订单 10010 当前状态是：待付款。";
            case "12345" -> "订单 12345 当前状态是：已签收。";
            default -> "未查询到订单 " + normalizedOrderId + " 的状态。";
        };
    }
}
```

## 为什么工具参数必须校验

用户说：

```text
帮我查一下订单 10086 的状态
```

模型理想输出：

```json
{
  "orderId": "10086"
}
```

但也可能输出：

```json
{
  "orderId": ""
}
```

或者：

```json
{
  "orderId": null
}
```

所以 Java 后端必须校验：

```text
arguments 是否存在
orderId 是否存在
orderId 是否为空
```

本课先做基础校验。权限、审计、高风险确认后续再做。
