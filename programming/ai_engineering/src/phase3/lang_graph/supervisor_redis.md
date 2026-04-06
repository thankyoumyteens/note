# 接入 Redis

我们在刚才的代码里使用的是 `MemorySaver()`。这只是一个 **“开发期玩具”**。它把大模型的状态快照存在了 Python 进程的本机内存里。想象一下，如果你的应用部署在多台服务器上（分布式架构），用户的第一句话打到了 A 机器，第二句话被负载均衡打到了 B 机器，B 机器的内存里根本没有 thread_id，系统瞬间就会“失忆”。如果你重启了服务器，所有用户的历史记录也会瞬间灰飞烟灭。

在以前的 LangChain 时代，你为了用 Redis，必须自己手写 RunnableWithMessageHistory，自己去拼装 JSON，自己去存取。

而在 LangGraph 的现代架构中，Redis 退居幕后，变成了一个纯粹的“存储驱动（Checkpointer）”。 官方为你写好了底层的序列化和存取逻辑，你只需要像换汽车轮胎一样，把 MemorySaver 拔下来，插上 RedisSaver 即可！

### 1. 安装依赖

```sh
pip install langgraph-checkpoint-redis
```

### 2. 代码

```py
import os
from typing import Annotated, Literal
from datetime import datetime

from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.redis import RedisSaver

import env_setup


@tool
def search_web(query: str) -> str:
    """当需要获取外部真实新闻、数据、事实时，调用此工具。"""
    print(f"\n[🌐 研究员行动] 正在全网检索：【{query}】...")
    from ddgs import DDGS
    import time
    import random
    try:
        time.sleep(random.uniform(0.5, 2.0))
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
        resp = "\n".join([f"摘要: {res['body']}" for res in results]) if results else "未找到外部信息。"
        print(f"检索结果：\n{resp}")
        return resp
    except Exception as e:
        print(f"[❌ 网络异常] 搜索词 {query} 遭遇拦截: {e}")
        return f"外网搜索失败: {e}"


tools = [search_web]


class TeamState(TypedDict):
    messages: Annotated[list, add_messages]
    next_action: str


llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3
)
llm_with_research_tools = llm.bind_tools(tools)


def researcher_node(state: TeamState):
    print("\n👉 [研究员接单] 开始分析并查阅资料...")
    current_time_str = datetime.now().strftime("%Y-%m-%d %A")
    sys_msg = SystemMessage(
        content="你是首席研究员。你的任务是收集详尽资料。\n"
                f"【核心设定：当前真实时间是 {current_time_str}】\n"
                f"如果你需要检索今天的实时数据，请务必在搜索词中带上真实的当前日期，而不是你记忆里的旧日期。\n"
                "⚠️ 强制网络风控限制：为了防止触发反爬虫，每次思考请【最多只能下发 1 个】搜索工具指令！"
                "如果需要查多个词，请在后续多轮对话中慢慢查。一旦你认为资料收集完毕，请用自然语言总结核心事实，不要再调用工具。"
    )
    messages = [sys_msg] + state["messages"]
    response = llm_with_research_tools.invoke(messages)

    return {"messages": [response]}


tool_node = ToolNode(tools)


def writer_node(state: TeamState):
    print("\n👉 [撰稿人接单] 拿到生肉资料，开始奋笔疾书...")
    current_time_str = datetime.now().strftime("%Y-%m-%d")
    sys_msg = SystemMessage(content=f"你是顶级的财经科技主笔。当前日期是 {current_time_str}。\n"
                                    f"你的任务是把研究员提供的资料，重写成一篇通俗易懂的微头条。严禁瞎编。")
    trigger_msg = HumanMessage(content="资料已全部就绪，请立刻根据上述信息开始撰写最终的文章！")
    messages = [sys_msg] + state["messages"] + [trigger_msg]
    response = llm.invoke(messages)
    print("✅ [撰稿人] 文章定稿！任务圆满结束。")
    return {"messages": [response]}


def researcher_router(state: TeamState) -> Literal["tools", "writer"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("🔀 [路由决策] 研究员申请调用工具，放行至 [tools] 节点。")
        return "tools"
    print("🔀 [路由决策] 研究员查阅完毕，放行至 [writer] 节点。")
    return "writer"


print("⚙️ 正在组装双 Agent 自动新闻流产线...")
workflow = StateGraph(TeamState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("tools", tool_node)
workflow.add_node("writer", writer_node)
workflow.add_edge(START, "researcher")
workflow.add_conditional_edges("researcher", researcher_router)
workflow.add_edge("tools", "researcher")
workflow.add_edge("writer", END)

# 🌟 连接到你公司的 Redis 集群
with RedisSaver.from_conn_string("redis://localhost:6379") as memory:
    # 🌟 第一次运行时，强制要求 Redis 创建 RediSearch 的底层索引！
    # 这就像是 Hibernate 的 ddl-auto=update 或者执行一次 Flyway/Liquibase 脚本
    memory.setup()

    # 编译图网络，现在它的记忆是分布式且持久化的了！
    app = workflow.compile(checkpointer=memory)

    # 后面的流转逻辑完全不变，连标点符号都不用改

    query = "去查一下今天特斯拉的最新新闻，然后帮我写一篇 300 字左右的微头条，风格要犀利一点。"
    print(f"\n👤 董事长下达最终需求: {query}")

    config = {"configurable": {"thread_id": "boss_task_1"}}
    initial_state = {"messages": [HumanMessage(content=query)]}

    for event in app.stream(initial_state, config=config):
        pass

    print("\n" + "=" * 50)
    print("🎉 董事长您好，最终成片文章如下：")
    print(app.get_state(config).values["messages"][-1].content)
    print("=" * 50)
```
