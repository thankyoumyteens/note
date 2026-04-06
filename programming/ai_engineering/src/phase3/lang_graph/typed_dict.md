# TypedDict

在 LangGraph 的代码里，TypedDict 是整个状态机（State）的基石。

在 Python 的原生世界里，字典（dict）就像是 Java 里的 `Map<String, Object>`。极其灵活，但也极其危险：你根本不知道里面到底存了什么 Key，也不知道 Value 是什么类型。写代码时，IDE 不会提示，拼写错了（比如把 messages 写成了 message）也只能等到运行时才抛出 KeyError。

TypedDict 就是 Python 官方为了拯救这种“裸奔”状态而引入的静态类型注解。对于 Java 开发者来说，你可以极其精准地把它理解为：一个极其轻量级的 DTO（数据传输对象）或 POJO。

一旦你用了 TypedDict，当你在 IDE（比如 PyCharm 或 VSCode）里敲出 `state["` 时，编辑器会瞬间弹出身代码提示，明确告诉你只有 messages 和 next_action 两个 Key 可以用。

```py
class TeamState(TypedDict):
    messages: Annotated[list, add_messages]
    next_action: str
```

⚠️ 注意：在 Python 里，TypedDict 仅仅是一个“静态分析工具”（给 IDE 和 mypy 等代码检查工具看的）。

在代码真正跑起来的瞬间（Runtime），TypedDict 会发生彻彻底底的类型擦除（Type Erasure）。在内存里，TeamState 会退化成一个最普通的 Python dict。它没有任何运行时的校验开销，也没有任何真正的强类型约束。

```py
# 💡 假设在运行时的某个角落，你写了极其离谱的代码：
state: TeamState = {"messages": 12345, "next_action": True, "hacker_key": "boom"}

# 运行时结果：Python 根本不会报错！它会毫无波澜地执行下去。
# (除非你提前运行了 mypy 等代码静态检查工具，它才会在运行前警告你)
```

所以，TypedDict 的核心价值在于 **“开发期的极其舒适”，而不是“运行期的绝对安全”**（如果需要运行期的绝对安全校验，Python 开发者会使用 Pydantic）。

## `messages: Annotated[list, add_messages]`

这行代码是整个 LangGraph 状态机能跑起来的“定海神针”。它解决了一个极其核心的架构问题：当多个节点并发向同一个状态写入数据时，到底是该“覆盖”还是“追加”？

在默认的 TypedDict 中，如果节点 A 返回了 `{"messages": ["你好"]}`，节点 B 返回了 `{"messages": ["世界"]}`，Python 字典的默认行为是无情覆盖。最终状态里只剩下“世界”。

但对话历史绝对不能被覆盖！它必须像日志一样不断追加。`Annotated[list, add_messages]` 就是用来打破“覆盖”规则的黑魔法。

1. `list`（基础类型）：告诉 IDE 和代码检查工具，messages 这个字段在内存里的绝对形态是一个列表。
2. `Annotated[...]`（元数据外衣）：这是 Python 官方 typing 模块提供的高级特性。它允许你在不改变变量基础类型的前提下，给它挂上一些“额外说明”。对于原生 Python 来说，它运行时会完全无视 Annotated 后面的东西；但 LangGraph 引擎在底层会去读取这个标签。
3. `add_messages`（合并函数）：这是 LangGraph 官方提供的一个具体函数（也就是 Reducer）。它告诉图引擎：“当任何节点试图给 messages 字段塞新数据时，绝对不要直接覆盖它，而是把旧数据和新数据一起传给 add_messages 函数，用这个函数的返回值作为最终状态。”

add_messages 底层其实是一个基于 ID 的 Upsert（更新或插入）引擎：

| 场景             | `add_messages` 的底层行为                                                                                      |
| :--------------- | :------------------------------------------------------------------------------------------------------------- |
| **正常对话追加** | 新消息没有 ID 或 ID 不重复 -> 直接 `append` 到列表末尾。                                                       |
| **流式输出更新** | 新消息带着与历史记录中某条消息 **相同的 ID** -> 将新内容与老内容 **拼接合并（Merge）**，而不是追加一条新记录。 |
| **开发环境重试** | 你手动把流程倒退回上一步重跑 -> 它会自动根据 ID 覆盖掉那条错误的消息，防止出现重复的脏数据。                   |
