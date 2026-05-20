# 为什么这一步很重要？

因为从现在开始，你的 AI Gateway 不只是：

```text
输入文本 -> 输出文本
```

而是变成：

```text
输入文本 -> 输出业务对象
```

这意味着后端可以继续处理：

```java
if (result.priority() == TaskPriority.HIGH) {
    // 创建高优先级任务
}

if (result.dueTimeText() != null) {
    // 进入时间解析流程
}
```

这就是 AI 应用和聊天机器人的分界线。

---

## 当前方案的不足

这一课的实现是“工程可用的基础版”，但还不是最终生产版。

它有几个问题：

## 1. Prompt 约束不是强约束

模型仍然可能输出：

```text
好的，以下是 JSON：
{
  ...
}
```

所以我们加了 `cleanupJson()`。

但更好的方案是使用模型原生 JSON Schema。OpenAI 的 Structured Outputs 可以让模型响应遵循指定 JSON Schema；function calling 也通过 JSON Schema 定义工具参数，让模型连接你的外部系统。

---

## 2. 没有自动修复

如果模型输出 JSON 解析失败，当前直接报错。

生产系统应该：

```text
第一次生成
 -> 解析失败
 -> 把错误和原始输出发回模型
 -> 要求修复为合法 JSON
 -> 再解析
 -> 仍失败才返回错误
```

这个后面会做。

---

## 3. 没有字段级置信度

真实信息抽取系统最好输出：

```json
{
  "taskName": {
    "value": "给张三发报价单",
    "confidence": 0.93
  }
}
```

但初学阶段先不加，避免复杂度过高。

---

## 4. 没有时间标准化

当前：

```json
{
  "dueTimeText": "明天下午三点"
}
```

后面要升级成：

```json
{
  "dueTimeText": "明天下午三点",
  "dueTime": "2026-05-03T15:00:00+08:00"
}
```

这个需要结合：

```text
当前日期
用户时区
自然语言时间解析
业务规则
```
