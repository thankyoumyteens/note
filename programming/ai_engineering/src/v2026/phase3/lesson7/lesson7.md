# 第 7 课：调用日志与成本统计

## 本课要解决什么问题

前面几课已经能调用模型，但现在有一个生产级问题：

```text
每次模型调用发生了什么，目前系统不知道。
```

你现在缺少这些信息：

```text
调用了哪个模型？
调用的是 chat / complete / tool decision / repairJson？
耗时多久？
成功还是失败？
失败原因是什么？
用了多少 token？
未来成本是多少？
```

一句话概括本课：

> 本课要记录每次模型调用的关键信息，为后续成本统计、Tracing、LLMOps、限流、fallback 打基础。

## 为什么 AI Gateway 必须记录调用日志？

传统后端接口通常会记录：

```text
请求路径
状态码
耗时
异常
用户 ID
traceId
```

AI Gateway 还需要额外记录：

```text
模型名称
调用类型
prompt token
completion token
total token
供应商
是否流式
是否成功
错误信息
```

因为大模型调用有几个特殊问题：

```text
1. 成本按 token 计费
2. 延迟通常比普通接口高
3. 供应商可能限流或失败
4. 模型输出不稳定
5. 不同模型价格和性能不同
6. 后续需要做 fallback 和 model routing
```

没有调用日志，就无法回答：

```text
今天模型调用了多少次？
哪个接口最耗 token？
哪个模型最慢？
哪个功能最贵？
失败率是多少？
结构化输出失败是否增多？
```

## 为什么调用日志不能记录完整 Prompt？

完整 Prompt 可能包含：

```text
用户隐私
业务数据
API 参数
内部 system prompt
文档内容
工具返回结果
```

所以本课先不保存完整 prompt，只保存：

```text
调用类型
模型名
耗时
token
状态
错误信息
```

生产系统如果要保存输入输出，也必须做：

```text
脱敏
权限控制
数据保留策略
审计
```

## 什么是调用类型 callType？

你的项目里已经有多种模型调用场景：

```text
普通聊天
任务抽取
JSON 修复
工具调用决策
```

它们都走 `LlmClient.complete()`，但业务含义不同。

所以需要记录调用类型：

```text
CHAT
TASK_EXTRACTION
JSON_REPAIR
TOOL_DECISION
```

以后你看到日志时，才能知道一次模型调用到底是在做什么。
