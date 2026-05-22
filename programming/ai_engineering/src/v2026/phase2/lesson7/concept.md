# 核心概念

## 什么是 Evals

Evals 可以理解为 AI 功能的测试集。

传统后端测试通常判断：

```text
输入 A -> 输出必须等于 B
```

AI 应用测试更复杂，因为模型输出具有概率性。

所以 evals 更关注：

```text
结构是否正确
字段是否命中
工具选择是否正确
关键参数是否正确
失败样本是什么
整体通过率是多少
```

如果没有 evals，你调 Prompt 只能靠感觉：

```text
这个回答好像不错
这个 Prompt 好像更稳定
这个模型好像更聪明
```

但企业级 AI 应用不能靠感觉。

你需要知道：

```text
结构化输出通过率：85% 还是 98%？
工具选择准确率：90% 还是 60%？
失败集中在哪些输入？
Prompt 修改后效果有没有回退？
```

所以从第 7 课开始，后续每次调整 Prompt、模型、JSON Schema、Tool Calling，都应该能跑一次 eval。

## 什么是 Golden Dataset

Golden Dataset 是人工定义的标准答案集。

例如结构化输出：

```json
{
  "id": "task-001",
  "input": "明天下午三点提醒我给张三发报价单，优先级高。",
  "expected": {
    "taskName": "给张三发报价单",
    "dueTimeText": "明天下午三点",
    "priority": "HIGH",
    "assignee": "me"
  }
}
```

工具调用：

```json
{
  "id": "tool-001",
  "input": "帮我查一下订单 10086 的状态",
  "expected": {
    "shouldCallTool": true,
    "toolName": "getOrderStatus",
    "orderId": "10086"
  }
}
```

Golden Dataset 不需要一开始很大。

本课先做：

```text
结构化输出 6 条
工具调用 6 条
```

后续逐步扩充。
