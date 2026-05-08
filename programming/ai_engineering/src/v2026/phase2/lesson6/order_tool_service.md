# 新增订单工具 Service

新建：

```text
service/OrderToolService.java
```

```java
package com.example.aigateway.service;

import org.springframework.stereotype.Service;

@Service
public class OrderToolService {

    public String getOrderStatus(String orderId) {
        if (orderId == null || orderId.isBlank()) {
            throw new IllegalArgumentException("orderId cannot be empty");
        }

        return switch (orderId.strip()) {
            case "10086" -> "订单 10086 当前状态是：已发货，预计明天送达。";
            case "10010" -> "订单 10010 当前状态是：待付款。";
            case "12345" -> "订单 12345 当前状态是：已签收。";
            default -> "未查询到订单 " + orderId + " 的状态。";
        };
    }
}
```

这里先用 Mock 数据。
真实项目中这里会调用：

```text
订单数据库
订单服务 API
ERP 系统
电商平台接口
```
