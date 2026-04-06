# MemorySaver

```py
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

在 LangGraph 中，memory（官方专业术语叫 Checkpointer / 检查点）绝对不是一个简单的“聊天记录拼接器”，它是整个图网络能够被称为“状态机”的灵魂。

如果不用 memory（即直接调用 `workflow.compile()`），你的图网络就是一个绝对无状态（Stateless）的纯函数。它跑完一遍，把结果吐给你，然后瞬间“失忆”。当你发第二句话时，它根本不知道你是谁、刚才查过什么资料。

当你传入 `checkpointer=memory` 时，你其实是给这套图网络外挂了一个 **“游戏自动存档引擎”**。

在底层，它赋予了你的 Agent 三大企业级“超能力”：

### 1. 多轮对话的“记忆锚点” (Context Retention)

还记得我们每次调用 `app.stream()` 时传的 `{"configurable": {"thread_id": "boss_task_1"}}` 吗？

有了 memory，当请求到来时，引擎会先去内存里通过这个 thread_id 把上次聊天的所有 messages 和 retry_count 捞出来，塞给图网络；当节点跑完后，它又会自动把最新的状态覆盖写回内存。

### 2. 断点续传与“人类介入” (Human-in-the-loop)

这是它最牛逼的地方！因为 memory 会在每一个 Node 执行完毕后，强制打一个快照（Snapshot）。

这就意味着，你可以配置图网络：“跑完 `[研究员节点]` 后，立刻暂停挂起（Suspend）！” 此时 Python 进程可以完全释放。等你（人类）喝完咖啡，或者审批通过后，带着那个 thread_id 发送一条继续指令，图网络会从 memory 里完美复活刚才的状态，无缝走向 `[撰稿人节点]`。

### 3. 时间漫游 (Time Travel)

因为 memory 记录的不是最终结果，而是每一步执行后的状态快照列表。在高级调试中，如果大模型在第 5 步写错了代码，你可以直接调用 API，把状态机“时光倒流”回第 4 步的快照，修改一下用户的 Prompt，然后让它从第 4 步重新分叉运行！
