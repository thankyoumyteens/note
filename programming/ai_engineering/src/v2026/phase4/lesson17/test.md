# 测试方式

### 创建工单

```bash
curl -X POST http://localhost:8080/api/agent/tickets \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-support-001" \
  -H "X-Roles: support" \
  -H "Content-Type: application/json" \
  --data-raw '{
    "title": "客户询问退款进度",
    "description": "客户说订单 ORDER-1001 已经申请退款，但迟迟没有收到退款。请检查订单并给出处理建议。"
  }'
```

---

### 第一次 run：生成结构化 plan

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-support-001" \
  -H "X-Roles: support"
```

预期：

```text
currentStep = PLAN
structuredPlan.requiredTool = checkOrder
structuredPlan.arguments.orderId = ORDER-1001
```

---

### 第二次 run：按 plan 调用工具

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-support-001" \
  -H "X-Roles: support"
```

预期：

```text
currentStep = CHECK_ORDER
orderCheckResult 有内容
toolCallCount = 1
```

---

### 测试工具权限不足

用没有权限的角色：

```bash
curl -X POST http://localhost:8080/api/agent/tickets/{ticketId}/run \
  -H "X-Tenant-Id: tenant-a" \
  -H "X-User-Id: user-guest-001" \
  -H "X-Roles: guest"
```

预期工具结果中出现：

```text
TOOL_PERMISSION_DENIED
```

---

### 测试工具调用次数限制

临时配置：

```yaml
ai:
  tool:
    max-tool-calls-per-workflow: 0
```

再次运行工具步骤。

预期：

```text
TOOL_CALL_LIMIT_EXCEEDED
```

测试完恢复：

```yaml
ai:
  tool:
    max-tool-calls-per-workflow: 5
```

---

### 运行 Tool Eval

```bash
cd python-tools
uv run python scripts/eval_tool_plan.py
```

预期：

```text
=== Tool Plan Eval Result ===
total: 2
passed: ...
failed: ...
pass_rate: ...
```
