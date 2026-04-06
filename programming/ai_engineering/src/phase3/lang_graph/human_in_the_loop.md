# 断点与人工介入

假设我们现在有一个业务链条：researcher -> writer -> publish_article（自动发布到外网的危险动作）。我们绝对不能让大模型直接发文，必须在 publish_article 之前卡住！

你只需要在代码里加上一个极其关键的参数：interrupt_before。Agent 就会在跑到断点处自动停下。

现在，我们像往常一样启动任务。你看下面这段代码，它完美模拟了“异步审批”的全过程：

```py
import uuid
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


# ==========================================
# 0. 前置准备：定义图纸和打断点
# ==========================================
class State(TypedDict):
    messages: Annotated[list, add_messages]


def writer_node(state: State):
    print("\n✍️ [撰稿人] 正在生成草稿...")
    # 模拟大模型生成的极其激进的草稿
    draft = AIMessage(content="【原版草稿】特斯拉这波彻底不行了，马斯克马上要完！")
    return {"messages": [draft]}


def publish_node(state: State):
    # 发布节点只负责无脑读取最后一条消息，推送到全网
    final_text = state["messages"][-1].content
    print(f"\n📢 [线上发布系统] 已成功将文章推送到头条！\n    最终内容 -> {final_text}")
    return {"messages": []}


workflow = StateGraph(State)
workflow.add_node("writer", writer_node)
workflow.add_node("publish", publish_node)
workflow.add_edge(START, "writer")
workflow.add_edge("writer", "publish")
workflow.add_edge("publish", END)

memory = MemorySaver()
# 🌟 挂载物理刹车：在进入 publish 之前强制拦截！
app = workflow.compile(
    checkpointer=memory,
    # 在进入这个节点前，强制冻结系统！
    interrupt_before=["publish"]
)

config = {"configurable": {"thread_id": "boss_approval_001"}}

# ==========================================
# 🚀 第一阶段：正常点火，自动刹车
# ==========================================
print("\n" + "=" * 50 + "\n[阶段 1] 任务启动\n" + "=" * 50)
inputs = {"messages": [HumanMessage(content="帮我写一篇特斯拉的微头条。")]}

for event in app.stream(inputs, config):
    pass  # 跑到 publish 之前会自动停止

print("🚦 系统已触发布发文前的断点保护！当前进程已安全挂起。")

# ==========================================
# 🔍 第二阶段：获取当前挂起状态
# ==========================================
print("\n" + "=" * 50 + "\n[阶段 2] 获取挂起状态\n" + "=" * 50)
# 相当于你在后台管理系统查询 pending 状态的工单
snapshot = app.get_state(config)

print(f"当前阻塞的节点: {snapshot.next}")  # 输出 ('publish',)
last_message = snapshot.values["messages"][-1]
print(f"🕵️ 董事长查阅待发草稿: {last_message.content}")

# ==========================================
# ✍️ 第三阶段：人工查阅并篡改内容
# ==========================================
print("\n" + "=" * 50 + "\n[阶段 3] 董事长开始修改\n" + "=" * 50)
print("📝 董事长觉得原文太激进，容易引发公关危机，大笔一挥进行修改...")

# 🌟 篡改魔法：构造一个带有【相同 ID】的新消息！
modified_message = AIMessage(
    content="【修改后草稿】特斯拉面临短期销量挑战，但其在自动驾驶领域的长期战略底座依然稳固。",
    id=last_message.id  # 👈 极其核心：拿着原消息的 ID 去覆盖它！
)

# 强制更新数据库（Checkpointer）里的快照
app.update_state(config, {"messages": [modified_message]})
print("✅ 修改已落盘！大模型的原版记忆已被彻底抹除覆盖。")

# ==========================================
# 🟢 第四阶段：下达继续指令 (Resume)
# ==========================================
print("\n" + "=" * 50 + "\n[阶段 4] 释放断点，继续执行\n" + "=" * 50)
print("🔘 点击【同意发布】按钮...")

# 🌟 传入 None，这样 LangGraph 、就会自动从 Checkpointer 里捞出上次的状态继续跑
for event in app.stream(None, config):
    pass
```
