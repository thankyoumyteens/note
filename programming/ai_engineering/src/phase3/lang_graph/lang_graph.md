# 复杂任务编排与多 Agent 协同

你在上一步手敲的那个“查天气”的 if-else 循环，叫做 单体 ReAct 脚本。它能跑通，但极其脆弱。

想象一下，如果大模型要在查天气之后，再去调另一个 API 订机票，中间机票 API 挂了需要重试，或者订票前需要人工点击确认（Human-in-the-loop）…… 你的 while 和 if-else 绝对会变成一座无法维护的代码屎山。

LangGraph 的核心思想，就是把 Agent 的运行逻辑“图论化（Graph）”：

1. State（状态）：相当于 Java 里的 `RequestContext` 或全局 DTO。它在整个图里流转，每个节点都可以读取和修改它。
2. Nodes（节点）：相当于 Java 里的 `@Service` 方法。就是一个个普通的 Python 函数，它们接收 State，执行业务逻辑（比如调用 LLM，或者执行 Tool），然后返回更新后的 State。
3. Edges（边）：相当于路由控制器。决定了执行完当前节点后，下一个该去哪个节点（支持条件判断，比如“如果 LLM 下发了 Tool_call，就走 Tool 节点，否则走向 END”）。
