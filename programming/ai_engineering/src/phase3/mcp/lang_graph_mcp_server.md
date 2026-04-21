# LangGraph 接入 MCP Server

### 1. 安装

为了让 LangGraph 听懂 MCP 协议，LangChain 官方专门发布了一个桥接包。请在终端执行：

```sh
pip install langchain-mcp-adapters
```

### 2. 代码

你不需要在 Agent 代码里写任何本地工具逻辑，甚至连远端 ERP 系统的接口参数是什么你都不需要知道。你只需要用 `MultiServerMCPClient` 作为 JDBC 连接池去“扫”一遍远端服务即可！

```py
import asyncio
import json
import os
from typing import Literal, TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode


import env_setup


class State(TypedDict):
    messages: Annotated[list, add_messages]


async def main():
    print("⚙️ [系统启动] 正在初始化 MCP 协议连接池...")

    # 🌟 核心魔法 1：建立连接池 (类似 JDBC DriverManager)
    # 我们使用 stdio 协议，直接在本地后台唤醒那个遗留系统的 Python 脚本
    client = MultiServerMCPClient({
        "my_legacy_erp": {
            "command": "python",
            # ⚠️ 注意：这里必须写你刚刚那个 legacy_order_server.py 的【绝对路径】
            "args": ["/your_path/legacy_order_server.py"],
            "transport": "stdio",
        }
    })

    # 🌟 核心魔法 2：动态反射！
    # 这一步，客户端通过网络向 Server 询问：“你有什么本领？”
    # MCP Adapter 会自动把远端返回的 JSON-RPC 格式，完美转换成 LangChain 的 @tool 格式数组！
    mcp_tools = await client.get_tools()
    print(f"🔗 成功挂载远端遗留系统 API: {[t.name for t in mcp_tools]}")

    # ---------------------------------------------------------
    # 👇 下面的代码，就是你极其熟悉的 LangGraph 标准流转逻辑了
    # ---------------------------------------------------------
    llm = ChatOpenAI(
        api_key=os.environ.get("API_KEY"),
        base_url="https://api.siliconflow.cn/v1",
        model="Qwen/Qwen3.6-35B-A3B"
    )
    llm_with_tools = llm.bind_tools(mcp_tools)

    def agent_node(state: State):
        safe_messages = []
        for msg in state["messages"]:
            if msg.type == "tool" and not isinstance(msg.content, str):
                # 有的大模型只要字符串，如果发现 MCP 返回了列表，就强行转成 JSON 字符串！
                msg.content = json.dumps(msg.content, ensure_ascii=False)
            safe_messages.append(msg)

        print("\n👉 [Agent] 正在思考...")
        response = llm_with_tools.invoke(safe_messages)
        return {"messages": [response]}

    # 官方的工具执行节点
    tool_node = ToolNode(mcp_tools)

    # 路由判断
    def should_continue(state: State) -> Literal["tools", "__end__"]:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "__end__"

    # ==========================================
    # 组装自定义图网络
    # ==========================================
    workflow = StateGraph(State)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")
    app = workflow.compile()

    # ==========================================
    # 执行测试
    # ==========================================
    query = "请帮我查一下旧版 ERP 系统里 ORD-002 的订单状态。"
    print(f"\n👤 董事长下达指令: {query}")
    inputs = {"messages": [HumanMessage(content=query)]}

    async for event in app.astream(inputs):
        for key, value in event.items():
            if "messages" in value:
                last_msg = value['messages'][-1]
                if last_msg.type == "tool":
                    print(f"   [底层 MCP 通信] 获取到数据: {last_msg.content}")
                elif last_msg.type == "ai" and last_msg.content:
                    print(f"\n🤖 Agent 最终汇报: {last_msg.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

当你运行这段代码时，你会发现你的 LangGraph Agent 瞬间具备了查询公司内网订单的能力。最恐怖的是，你的 LangGraph 脚本里，没有任何一行关于“订单”、“数据库”的业务逻辑。

这意味着：

1. 彻底解耦：如果明天公司决定把遗留订单系统从 Python 换成 Java，或者接口字段变了，你的 LangGraph AI 代码连一个标点符号都不需要改。你只需要让后端团队去改 MCP Server 里的映射逻辑就行了。
2. 无限扩展：你可以给 MultiServerMCPClient 传入十几个微服务的地址。Agent 的大脑在本地，但它的手脚已经通过 MCP 协议，延伸到了公司机房的每一个角落。
