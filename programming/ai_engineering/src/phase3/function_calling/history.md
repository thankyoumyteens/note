# RunnableWithMessageHistory 光荣退役

在阶段二（单纯的 RAG 问答链）中，RunnableWithMessageHistory 是极其完美的。因为那时候的输入输出是线性且简单的：
用户问(HumanMessage) -> 数据库查 -> 模型答(AIMessage)。
历史记录里只有干干净净的人机对话。

但在阶段三的 Agent 时代，历史记录（Messages）变“脏”了，也变“复杂”了。
为了让 Agent 成功调用工具，历史记录里插入了大量的 AIMessage (附带 tool_calls) 和 ToolMessage (附带执行结果)。

如果你强行把现在的 Agent 塞进之前的 RunnableWithMessageHistory 里，会遇到两个极其头疼的问题：

1. 记忆污染与 Token 爆炸：Agent 在后台疯狂调工具（比如查了 3 次天气、搜了 2 次网页），这些带着极其冗长 JSON 数据和网页源码的 ToolMessage 会全部被 Redis 缓存下来。你的 Token 会在几轮对话内瞬间原地爆炸！
2. 截断导致的“死锁”：咱们之前写过一个“达到 4 条就滚动总结”的异步并发锁逻辑。但如果是 Agent，它可能一轮思考就产生了 3 条内部消息。如果你用旧的逻辑去粗暴裁剪（只留 Summary），Agent 会瞬间丢失它刚才调用的 tool_call_id，下一秒直接给你抛出极其致命的 API 报错。

## 架构的升维：从“外挂历史”到“状态机检查点 (Checkpointer)”

这就是为什么要 **“全面转向基于图（Graph）的编排方式（LangGraph）”**。

在最新的 LangGraph 架构中，我们抛弃了 RunnableWithMessageHistory 这种“外挂式”的记忆拦截器。取而代之的是一个更加原生、更具统治力的概念：状态 (State) 与 检查点 (Checkpointer)。

- 以前的 RunnableWithMessageHistory 就像是 Spring AOP (拦截器)，在请求前后强行读取/写入 Redis。
- 现在的 LangGraph State 就像是极其严谨的 ThreadLocal 或者 Redux Store。整个 Agent 就是一个状态机，messages 只是状态机里的一个变量。我们不需要拦截器，我们只需要在状态机的每一次节点流转完后，把整个状态机“快照（Snapshot）”持久化到数据库里即可（这就是 Checkpointer）。
