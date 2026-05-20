# 测试

## 正常场景

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"明天下午三点提醒我给张三发报价单，优先级高。"}'
```

预期：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

---

## 低优先级

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"有空的时候帮我整理一下上周的会议纪要，不急。"}'
```

预期重点：

```json
{
  "priority": "LOW"
}
```

## 指定负责人

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"让李四今天下班前提交测试报告。"}'
```

预期重点：

```json
{
  "taskName": "提交测试报告",
  "dueTimeText": "今天下班前",
  "assignee": "李四"
}
```

## 无时间

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"帮我整理客户需求文档。"}'
```

预期重点：

```json
{
  "dueTimeText": null,
  "assignee": "me"
}
```
