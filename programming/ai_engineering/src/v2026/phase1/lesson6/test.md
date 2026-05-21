# 测试

## 查询存在的订单

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"帮我查一下订单 10086 的状态"}'
```

预期：

```json
{
  "answer": "订单 10086 当前状态是：已发货，预计明天送达。"
}
```

---

## 查询另一个订单

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"订单 10010 现在怎么样？"}'
```

预期：

```json
{
  "answer": "订单 10010 当前状态是：待付款。"
}
```

---

## 查询不存在的订单

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"查一下订单 99999"}'
```

预期：

```json
{
  "answer": "未查询到订单 99999 的状态。"
}
```

---

## 非订单问题

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请解释一下什么是 RAG"}'
```

预期类似：

```json
{
  "answer": "我只能处理订单状态查询相关请求。"
}
```
