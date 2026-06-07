# 测试方式

### 创建工单

```bash
curl -X POST http://localhost:8080/api/agent/tickets \
  -H "Content-Type: application/json" \
  --data-raw '{
    "title": "客户询问退款进度",
    "description": "客户说订单 ORDER-1001 已经申请退款，但迟迟没有收到退款。请检查订单并给出处理建议。"
  }'
```

预期：

```text
status = CREATED
currentStep = CREATED
stepCount = 0
```

记录返回的 `ticketId`。

---

### 第一次 run：生成计划

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run
```

预期：

```text
status = RUNNING
currentStep = PLAN
stepCount = 1
plan 有内容
```

---

### 第二次 run：检查订单

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run
```

预期：

```text
currentStep = CHECK_ORDER
orderCheckResult 有内容
```

---

### 第三次 run：生成回复草稿

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run
```

预期：

```text
currentStep = DRAFT_REPLY
draftReply 有内容
```

---

### 第四次 run：进入人工审核

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run
```

预期：

```text
status = WAITING_HUMAN_REVIEW
currentStep = HUMAN_REVIEW
```

---

### 提交人工审核通过

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/human-review \
  -H "Content-Type: application/json" \
  --data-raw '{
    "approved": true,
    "comment": "确认没有重复退款，可以按草稿回复客户。"
  }'
```

预期：

```text
status = COMPLETED
currentStep = COMPLETE
summary 有内容
```

---

### 提交人工审核拒绝

新建另一个 ticket，跑到 `WAITING_HUMAN_REVIEW` 后：

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/human-review \
  -H "Content-Type: application/json" \
  --data-raw '{
    "approved": false,
    "comment": "需要进一步核对财务系统。"
  }'
```

预期：

```text
status = FAILED
currentStep = FAIL
summary = Workflow rejected by human reviewer.
```

---

### 测试 step limit

临时改小：

```yaml
ai:
  agent:
    max-steps: 2
```

连续调用 run。

预期：

```text
status = STEP_LIMIT_EXCEEDED
currentStep = FAIL
```

测试完成后恢复：

```yaml
ai:
  agent:
    max-steps: 6
```
