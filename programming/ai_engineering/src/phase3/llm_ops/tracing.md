# 给 Python 客户端加上探针(V3)

在你的 Python 项目根目录下，修改或创建 `.env` 文件（这是绝对核心的一步）：

```conf
# 填入你刚才在本地 3003 端口生成的 Key
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
# 把探头数据打到本地容器！
LANGFUSE_HOST=http://localhost:3003
```

### 1. 安装依赖

```sh
pip install langfuse
```

### 2. 代码

```py
import asyncio
import json
import os
from typing import Literal, TypedDict, Annotated

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
# 🌟 核心改动 1：引入 Langfuse 的 LangChain 专属回调处理器
from langfuse.langchain import CallbackHandler

# 确保环境变量已经加载 (包含 LANGFUSE_HOST 等)
import env_setup


class State(TypedDict):
    messages: Annotated[list, add_messages]


async def main():
    print("⚙️ [系统启动] 正在初始化 MCP 协议连接池...")
    client = MultiServerMCPClient({
        "java_erp_microservice": {
            "url": "http://127.0.0.1:8080/mcp",
            "transport": "http",
        }
    })
    mcp_tools = await client.get_tools()
    print(f"🔗 成功挂载远端遗留系统 API: {[t.name for t in mcp_tools]}")

    llm = ChatOpenAI(
        api_key=os.environ.get("API_KEY"),
        base_url="https://api.siliconflow.cn/v1",
        model="Qwen/Qwen3.6-35B-A3B"
    )
    llm_with_tools = llm.bind_tools(mcp_tools)

    # 🌟 核心改动 2：初始化 Langfuse 回调探针
    # 它会自动读取你本地 .env 文件中的 PUBLIC_KEY, SECRET_KEY 和 HOST
    langfuse_handler = CallbackHandler()

    def agent_node(state: State):
        safe_messages = []
        for msg in state["messages"]:
            if msg.type == "tool" and not isinstance(msg.content, str):
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

    # 🌟 核心改动 3：在执行流的入口，把探针作为全局配置塞进去！
    # 这一步极其致命，它相当于给整个图网络戴上了听诊器
    config = {"callbacks": [langfuse_handler]}

    async for event in app.astream(inputs, config=config):
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

### 3. 验收

运行你的 Python 脚本。

脚本跑完后，**切回浏览器的 Langfuse 后台页面，点击左侧的 "Traces"**。

你将亲眼看到一条崭新的记录躺在那里。点开它，你就能看到一个极其清晰的树状图。
