# 第 6 课：Function Calling / Tool Calling

前面第 4、5 课已经完成：

```text
自然语言输入
  -> 模型输出 JSON
  -> Java DTO
```

现在要进一步升级：

```text
自然语言输入
  -> 模型判断是否需要调用工具
  -> 输出工具名称和参数
  -> Java 后端执行工具
  -> 返回工具执行结果
```

一句话概括：

> 本课实现一个订单助手接口，让模型判断用户是否要查询订单，并由 Java 后端安全执行 `getOrderStatus` 工具。

最终新增接口：

```http
POST /api/ai/order-assistant
```

示例请求：

```json
{
  "message": "帮我查一下订单 10086 的状态"
}
```

示例响应：

```json
{
  "answer": "订单 10086 当前状态是：已发货，预计明天送达。"
}
```
