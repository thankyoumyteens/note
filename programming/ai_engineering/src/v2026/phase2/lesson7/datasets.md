# 创建评估集

本课先评估：

```text
/api/ai/extract-task 的字段结果
/api/ai/order-assistant 的最终回答是否符合预期
```

但要注意：

`/api/ai/order-assistant` 当前返回的是自然语言 `answer`，不是工具调用决策本身，所以本课的工具调用评估先采用“黑盒评估”：

```text
输入订单问题
  -> 调接口
  -> 看最终 answer 是否包含预期订单状态
```

更理想的生产评估应该暴露调试接口或记录内部 tool decision，例如：

```text
shouldCallTool
toolName
arguments.orderId
```

这会放到后续 AI Gateway 生产化阶段处理。

## 创建结构化输出评估集

文件：

```text
evals/datasets/task_extraction_cases.jsonl
```

内容：

```jsonl
{"id":"task-001","input":"明天下午三点提醒我给张三发报价单，优先级高。","expected":{"taskName":"给张三发报价单","dueTimeText":"明天下午三点","priority":"HIGH","assignee":"me"}}
{"id":"task-002","input":"有空的时候帮我整理一下上周的会议纪要，不急。","expected":{"taskName":"整理上周的会议纪要","dueTimeText":null,"priority":"LOW","assignee":"me"}}
{"id":"task-003","input":"让李四今天下班前提交测试报告。","expected":{"taskName":"提交测试报告","dueTimeText":"今天下班前","priority":"UNKNOWN","assignee":"李四"}}
{"id":"task-004","input":"帮我整理客户需求文档。","expected":{"taskName":"整理客户需求文档","dueTimeText":null,"priority":"UNKNOWN","assignee":"me"}}
{"id":"task-005","input":"明早九点提醒王五开项目评审会，很紧急。","expected":{"taskName":"开项目评审会","dueTimeText":"明早九点","priority":"HIGH","assignee":"王五"}}
{"id":"task-006","input":"下周一把发票整理好发给财务。","expected":{"taskName":"把发票整理好发给财务","dueTimeText":"下周一","priority":"UNKNOWN","assignee":"me"}}
```

说明：

```text
JSONL = 每一行是一个独立 JSON。
适合做批量测试数据。
```

---

## 创建订单助手评估集

文件：

```text
evals/datasets/order_assistant_cases.jsonl
```

内容：

```jsonl
{"id":"order-001","input":"帮我查一下订单 10086 的状态","expected":{"shouldContain":"订单 10086 当前状态是：已发货"}}
{"id":"order-002","input":"订单 10010 现在怎么样？","expected":{"shouldContain":"订单 10010 当前状态是：待付款"}}
{"id":"order-003","input":"查一下订单 12345","expected":{"shouldContain":"订单 12345 当前状态是：已签收"}}
{"id":"order-004","input":"查一下订单 99999","expected":{"shouldContain":"未查询到订单 99999 的状态"}}
{"id":"order-005","input":"请解释一下什么是 RAG","expected":{"shouldContain":"我只能处理订单状态查询"}}
{"id":"order-006","input":"今天天气怎么样？","expected":{"shouldContain":"我只能处理订单状态查询"}}
```

这个评估集先评估最终结果，而不是内部工具决策。
