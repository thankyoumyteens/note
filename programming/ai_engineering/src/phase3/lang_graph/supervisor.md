# 多 Agent 协同

在单体 Agent 时代，大模型既当爹又当妈。它既要构思大纲（规划），又要去网上查资料（执行），最后还要自己总结成文。这会导致一个极其致命的问题： **上下文污染和幻觉叠加。** 大模型脑子里的任务太多，走着走着就忘了自己最初的目标。

解决这个问题的终极方案，就是借鉴人类社会的公司组织架构。

在 LangGraph 中，最经典的多 Agent 协同架构是 Supervisor 模式（主管-员工模式）：

- Supervisor Agent（主管）：不干脏活累活。它的任务只有两个：拆解用户的大需求，然后把子任务分派给底下的打工人。
- Worker Agents（员工）：术业有专攻。比如“Researcher（研究员）”专门负责全网爬数据，“Coder（程序员）”专门写代码，“Reviewer（质检员）”专门找 Bug。
- Graph 路由（流转规则）：员工干完活后，必须把结果汇报给 Supervisor，由 Supervisor 决定是继续派活，还是收工把最终结果给用户。

## 实战

为了让你最直观地感受到多 Agent 的威力，我们来打造一个小型的“自动写稿工作室”。

- 角色 A：Researcher（研究员），它有一把名叫 search_web 的鸭鸭杀武器，专门去网上查最新资料。
- 角色 B：Writer（撰稿人），它没有任何武器，但它的 System Prompt 是顶级的财经博主，负责把杂乱的资料写成引人入胜的爆款文章。

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
from langgraph.checkpoint.memory import MemorySaver

import env_setup


# ==========================================
# 1. 武器库 (加入防抖与熔断机制)
# ==========================================
@tool
def search_web(query: str) -> str:
    """当需要获取外部真实新闻、数据、事实时，调用此工具。"""
    print(f"\n[🌐 研究员行动] 正在全网检索：【{query}】...")
    from ddgs import DDGS
    import time
    import random
    try:
        # 🌟 防线 1：随机休眠 (Jitter)，让并发的多线程错峰发起请求，骗过搜索引擎防火墙
        time.sleep(random.uniform(0.5, 2.0))

        # 🌟 防线 2：使用 with 语法安全管理网络连接，防止泄露
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))

        resp = "\n".join([f"摘要: {res['body']}" for res in results]) if results else "未找到外部信息。"
        print(f"检索结果：\n{resp}")
        return resp
    except Exception as e:
        print(f"[❌ 网络异常] 搜索词 {query} 遭遇拦截: {e}")
        return f"外网搜索失败: {e}"


tools = [search_web]


# ==========================================
# 2. 全局状态 (State) - 流水线上的“公司共享网盘”
# ==========================================
# 为了让你看懂底层原理，我们手写一个状态类：
class TeamState(TypedDict):
    # 消息记录
    messages: Annotated[list, add_messages]
    # 动态流转标记：告诉下一棒是谁接手
    next_action: str


# ==========================================
# 3. 大脑中枢初始化
# ==========================================
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.3
)
llm_with_research_tools = llm.bind_tools(tools)


# ==========================================
# 4. 定义员工节点 (Nodes)
# ==========================================
# 员工 A：研究员（带武器）
def researcher_node(state: TeamState):
    print("\n👉 [研究员接单] 开始分析并查阅资料...")
    # 获取真实的当前时间，并格式化为易读的字符串
    current_time_str = datetime.now().strftime("%Y-%m-%d %A")
    sys_msg = SystemMessage(
        content="你是首席研究员。你的任务是收集详尽资料。\n"
                f"【核心设定：当前真实时间是 {current_time_str}】\n"  # 👈 将时钟注入系统设定！
                f"如果你需要检索今天的实时数据，请务必在搜索词中带上真实的当前日期，而不是你记忆里的旧日期。\n"
                "⚠️ 强制网络风控限制：为了防止触发反爬虫，每次思考请【最多只能下发 1 个】搜索工具指令！"
                "如果需要查多个词，请在后续多轮对话中慢慢查。一旦你认为资料收集完毕，请用自然语言总结核心事实，不要再调用工具。"
    )
    # 每次请求，在历史消息最前面塞入系统人设指令
    messages = [sys_msg] + state["messages"]

    response = llm_with_research_tools.invoke(messages)

    # 极其干净：只管把 AI 的回复(无论是一句话还是工具指令)存入状态
    return {"messages": [response]}


# 🌟 直接实例化官方 ToolNode，它会自动处理所有底层序列化和报错拦截！
tool_node = ToolNode(tools)


# 员工 B：撰稿人（纯文字输出，无武器）
def writer_node(state: TeamState):
    print("\n👉 [撰稿人接单] 拿到生肉资料，开始奋笔疾书...")
    # 撰稿人也需要时间感知，这样写出来的文章才会有“就在今天”的新鲜感
    current_time_str = datetime.now().strftime("%Y-%m-%d")

    sys_msg = SystemMessage(content=f"你是顶级的财经科技主笔。当前日期是 {current_time_str}。\n"
                                    f"你的任务是把研究员提供的资料，重写成一篇通俗易懂的微头条。严禁瞎编。")
    # 强行在对话末尾加一句 HumanMessage，让 API 引擎以为人类在催更，强制其开口！
    trigger_msg = HumanMessage(content="资料已全部就绪，请立刻根据上述信息开始撰写最终的文章！")

    messages = [sys_msg] + state["messages"] + [trigger_msg]

    response = llm.invoke(messages)
    print("✅ [撰稿人] 文章定稿！任务圆满结束。")
    # 撰稿人干完活后，标记流转结束
    return {"messages": [response]}


# ==========================================
# 5. 定义图网络交警 (Conditional Edge)
# ==========================================
def researcher_router(state: TeamState) -> Literal["tools", "writer"]:
    last_message = state["messages"][-1]

    # 如果研究员最后输出的是工具调用指令，流向 ToolNode
    if last_message.tool_calls:
        print("🔀 [路由决策] 研究员申请调用工具，放行至 [tools] 节点。")
        return "tools"

    # 如果没有工具指令，说明研究员认为资料查完了，并给出了文字总结，流向撰稿人
    print("🔀 [路由决策] 研究员查阅完毕，放行至 [writer] 节点。")
    return "writer"


# ==========================================
# 6. 编排并编译图网络
# ==========================================
print("⚙️ 正在组装双 Agent 自动新闻流产线...")
workflow = StateGraph(TeamState)

# 注册节点
workflow.add_node("researcher", researcher_node)
workflow.add_node("tools", tool_node)
workflow.add_node("writer", writer_node)

# 起点必须是研究员
workflow.add_edge(START, "researcher")
# 研究员干完活后，走路由决定下一步
workflow.add_conditional_edges("researcher", researcher_router)
# 工具干完活，必须强制把结果还给研究员！
workflow.add_edge("tools", "researcher")
# 撰稿人写完，流程彻底结束
workflow.add_edge("writer", END)

# 挂载原生记忆沙盒
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# ==========================================
# 7. 投入任务测试！
# ==========================================
query = "去查一下今天特斯拉的最新新闻，然后帮我写一篇 300 字左右的微头条，风格要犀利一点。"
print(f"\n👤 董事长下达最终需求: {query}")

# 定义好这把唯一的记忆钥匙
config = {"configurable": {"thread_id": "boss_task_1"}}
initial_state = {"messages": [HumanMessage(content=query)]}

# 监控协同过程
for event in app.stream(initial_state, config=config):
    pass  # 节点内部有 print，这里可以直接 pass

print("\n" + "=" * 50)
print("🎉 董事长您好，最终成片文章如下：")
# 拿着同一把钥匙去捞取最终报告
print(app.get_state(config).values["messages"][-1].content)
print("=" * 50)
```

运行它！你会看到极其科幻的一幕在你的终端里发生：

1. 董事长（你） 下达一个宏大的需求。
2. 研究员 立刻接单，它敏锐地察觉到自己需要最新数据，于是拔出鸭鸭杀武器，冲到网上扒回来一堆干瘪的 JSON 和新闻摘要。然后它把这些“生肉”扔到了共享网盘（State）里，并把 next_action 改成 writer。
3. 路由交警 看到 writer 标记，立刻把流程导向撰稿人。
4. 撰稿人 拿到生肉资料，切换成它专属的“财经博主”人格，开始疯狂润色。润色完毕，交警指引走向 END。

在这个架构下，幻觉被极其有效地物理隔绝了！ 撰稿人根本没有联网的能力，它只能老老实实看着研究员查回来的客观数据进行扩写；而研究员不需要去思考怎么把文字写得优美，它只管死磕搜索精准度。
