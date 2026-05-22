# 测试方式

## 先启动 Java 服务

在项目根目录执行：

```bash
mvn spring-boot:run
```

确认这些接口可用：

```http
POST /api/ai/extract-task
POST /api/ai/order-assistant
```

---

## 运行结构化输出评估

在项目根目录执行：

```bash
python evals/scripts/eval_task_extraction.py
```

预期输出类似：

```text
[PASS] task-001
[PASS] task-002
[FAIL] task-003: ["taskName: expected='提交测试报告', actual='让李四提交测试报告'"]

=== Task Extraction Eval Result ===
total: 6
passed: 5
failed: 1
pass_rate: 83.33%
```

失败样本会写入：

```text
evals/reports/task_extraction_failures.jsonl
```

## 运行订单助手评估

```bash
python evals/scripts/eval_order_assistant.py
```

预期输出类似：

```text
[PASS] order-001
[PASS] order-002
[PASS] order-003
[PASS] order-004
[PASS] order-005
[PASS] order-006

=== Order Assistant Eval Result ===
total: 6
passed: 6
failed: 0
pass_rate: 100.00%
```

失败样本会写入：

```text
evals/reports/order_assistant_failures.jsonl
```

---

## 如何看待失败样本

失败不一定说明系统错了。

例如：

```text
expected taskName = 提交测试报告
actual taskName = 让李四提交测试报告
```

这可能只是 expected 写得太严格。

你需要判断：

```text
是 Prompt 错？
是模型输出可接受？
是 expected 应该放宽？
是比较逻辑应该改成 contains？
```

Evals 的重点不是追求一开始 100%，而是能发现问题、记录问题、持续改进。

---

## 当前不要做的事

本课不要急着：

```text
改 Prompt
引入 JSON Schema Structured Outputs
接入 RAGAS
做 dashboard
做 tracing
接入 CI/CD
```

这些都在后续课程。

本课只做到：

```text
有评估集
能批量跑
能统计通过率
能记录失败样本
```
