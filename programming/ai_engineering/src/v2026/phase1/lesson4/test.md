# 测试接口

执行：

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"明天下午三点提醒我给张三发报价单，优先级高。"}'
```

预期输出：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

再测几个：

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"有空的时候帮我整理一下上周的会议纪要，不急。"}'
```

预期：

```json
{
  "taskName": "整理上周的会议纪要",
  "dueTimeText": null,
  "priority": "LOW",
  "assignee": "me"
}
```

---

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"让李四今天下班前提交测试报告。"}'
```

预期：

```json
{
  "taskName": "提交测试报告",
  "dueTimeText": "今天下班前",
  "priority": "UNKNOWN",
  "assignee": "李四"
}
```
