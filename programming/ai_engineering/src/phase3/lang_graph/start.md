# 用 LangGraph 重构“查天气”工具

在单体脚本里，你为了让大模型调用工具，手写了极其臃肿的 `if ai_response.tool_calls:` 循环，还要自己去 invoke 本地函数、拼装 ToolMessage。

在真正的工业级开发中，我们绝不手写这些脏活累活。LangGraph 引入了两个极其强大的概念来接管这一切：

- 预置工具节点 (ToolNode)：官方写好的一个标准节点，你只要把 `[get_weather]` 这个函数列表扔给它，它就会自动帮你解析 LLM 的指令、执行代码、包装成 ToolMessage，甚至连抛错都能自动处理！
- 条件边 (Conditional Edge)：它就像是一个十字路口的交警，根据上一个节点的输出（State），瞬间决定下一步是走向 tools 节点，还是直接走向 END。

### 1. 安装依赖

```sh
pip install langgraph
```

### 2. 代码

```py
import os
from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# 🌟 引入 LangGraph 核心组件
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# 导入你的环境变量 (确保 API_KEY 已配置)
import env_setup


# ==========================================
# 1. 定义底层工具 (Tool)
# ==========================================
@tool
def get_weather(location: str) -> str:
    """获取指定城市的天气情况。"""
    print(f"\n[🔧 物理世界执行] 正在查询【{location}】的实时天气...")
    mock_db = {"北京": "晴天，25℃", "上海": "雷阵雨，28℃，建议带伞"}
    return mock_db.get(location, "未知天气信息")


tools = [get_weather]

# ==========================================
# 2. 初始化大模型并绑定武器 (LLM)
# ==========================================
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)


# ==========================================
# 3. 定义图网络的节点 (Nodes)
# ==========================================
# 节点 A：大脑中枢（负责思考和下发指令）
def call_model(state: MessagesState):
    print("\n👉 [节点: call_model] 大脑开始阅读当前上下文...")
    response = llm_with_tools.invoke(state["messages"])
    # 把它 append 进状态流里
    return {"messages": [response]}


# 节点 B：四肢动作（直接使用官方的 ToolNode，它会自动遍历并执行所有绑定的函数）
tool_node = ToolNode(tools)


# ==========================================
# 4. 🌟 定义动态路由 (Conditional Edge)
# ==========================================
# 这个函数就是交警，决定流程图的走向
def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state['messages']
    last_message = messages[-1]

    # 如果大脑的最后一条消息里包含了“工具调用”指令，把流程导向工具节点
    if last_message.tool_calls:
        print("🔀 [路由决策] 捕捉到工具调用指令，将状态流转至 [tools] 节点...")
        return "tools"

    # 如果没有，说明大脑已经得出了最终结论，直接结束图的运转
    print("🔀 [路由决策] 无工具调用需求，直接结束任务，流向 END。")
    return "__end__"


# ==========================================
# 5. 编排图网络图纸 (Graph)
# ==========================================
workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# 第一步：开始后，强制走向大脑节点
workflow.add_edge(START, "agent")

# 第二步：大脑思考完后，来到十字路口，由 should_continue 决定去哪
workflow.add_conditional_edges("agent", should_continue)

# 第三步：工具执行完毕后，强制回传给大脑，让大脑根据工具拿到的数据重新组织语言！
workflow.add_edge("tools", "agent")

# 编译并挂载原生记忆沙盒
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# ==========================================
# 6. 点火运行
# ==========================================
print("🚀 点火！装载记忆引擎并投入测试任务...")
config = {"configurable": {"thread_id": "user_agent_007"}}
inputs = {"messages": [HumanMessage(content="我明天要去上海，需要带伞吗？")]}

# 监控图节点的流转过程
for event in app.stream(inputs, config=config):
    for node_name, value in event.items():
        print(f"✅ [{node_name}] 节点执行完毕。")

print("\n🎉 大模型最终对用户说的回答:")
print(app.get_state(config).values["messages"][-1].content)
```

当你运行这段代码时，你会看到控制台里的流转日志极其优雅：

1. call_model 节点执行，决定调工具。
2. 触发 should_continue 路由，走向 tools。
3. tools 节点自动完成了你之前手写几十行的执行与消息封装。
4. 流程强制回到 call_model，LLM 看到数据，生成最终答案。
5. 触发 should_continue 路由，走向 END。

这种“让代码控制流程，让大模型只负责思考”的架构，从根本上消灭了长链路任务容易跑偏的弊病。
