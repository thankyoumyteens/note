# 引入“自愈 (Self-Healing)”机制

在 Java 后端的世界里，代码是 **绝对确定（Deterministic）** 的。你写了 `return new User()`，它就绝对不可能返回一个 `Order`。如果下游接口返回了无法反序列化的脏数据，你的标准做法是：抛出 JSONParseException -> 记录 Error 日志 -> 给前端返回 HTTP 500。

但在 Agent 架构中，大模型是 **非确定性（Non-deterministic）** 的。哪怕你用了 OpenAI 最顶级的模型，哪怕你开启了 json_mode，它依然有 0.1% 的概率会抽风——比如在 JSON 外面套了一层 Markdown 的 ````json` 标签，或者漏掉了一个逗号。

如果你沿用 Java 的思维直接抛异常崩溃，你的 AI 系统在生产环境中的可用性将永远无法超过 99%。

自愈机制（Self-Healing），就是赋予系统一个 **“高智商的 catch 块”**：不报错，不崩溃，而是把错误堆栈拍在大模型脸上，让它自己改 bug。

## 企业级自愈架构的三大主流形态

在 LangGraph 和现代 Agent 开发中，自愈机制通常分为三个层级，层层递进：

### 1. 节点内拦截（The Try-Catch Feedback Loop）

这就是咱们刚刚在代码里手写的那种。它最简单，也最常用。

- 执行逻辑：在当前 Node 内部，拦截序列化框架（如 Pydantic）抛出的异常。
- 黑魔法：将异常堆栈（Stack Trace）包装成一条带有压迫感的 HumanMessage 强行塞入历史记录。
- Prompt 话术规范：企业级实践中，报错 Prompt 必须包含三个核心要素：
  - 定性错误：“你刚才输出的格式完全错了。”
  - 提供线索：“这是底层解析器的报错日志：`[插入 error_msg]`。”
  - 重申规则：“请严格按照之前的 JSON Schema 重新输出，不要包含任何多余字符。”

```py
def researcher_node(state: TeamState):
    print("\n👉 [研究员接单] 开始分析并查阅资料...")
    current_time_str = datetime.now().strftime("%Y-%m-%d %A")
    sys_msg = SystemMessage(
        content="你是首席研究员。你的任务是收集详尽资料。\n"
                f"【核心设定：当前真实时间是 {current_time_str}】\n"
                f"如果你需要检索今天的实时数据，请务必在搜索词中带上真实的当前日期。\n"
                "⚠️ 强制网络风控限制：每次思考请【最多只能下发 1 个】搜索工具指令！查阅完毕后，请总结核心事实，不要再调用工具。"
    )
    messages = [sys_msg] + state["messages"]

    # 🌟 引入企业级 Agent 的“自愈 (Self-Healing)”机制
    try:
        response = llm_with_research_tools.invoke(messages)
    except Exception as e:
        # 如果捕获到 Pydantic 格式校验报错，不要让程序崩溃！
        print(f"\n[⚠️ 触发自愈机制] 模型下发的工具指令格式有误，强行打回重做...")

        # 将错误原因包装成 HumanMessage，像老板骂员工一样扔回给大模型
        error_msg = HumanMessage(
            content=f"系统错误：你的工具调用格式校验失败。必须返回标准的 JSON 对象字典，不能是字符串或其他格式！底层报错：{str(e)}。请立即自我修正并重新输出！"
        )
        # 带着报错信息，强迫它再思考一次
        response = llm_with_research_tools.invoke(messages + [error_msg])

    return {"messages": [response]}
```

### 2. 工具执行自愈（Tool Call Self-Correction）

大模型格式输对了，但传错了业务参数。比如你要查 `get_weather(city_code)`，它给你传了个中文的 "北京"。此时本地 Python 函数会抛出 ValueError。

- LangGraph 的官方方案：官方的 ToolNode 其实自带了自愈能力。
- 底层行为：当 ToolNode 抓到 Python 代码异常时，它不会让图崩溃，而是会生成一条包含错误信息的 `ToolMessage(content="Error: xxx", tool_call_id="...")` 传回给图网络。
- 流转闭环：大模型（researcher_node）接到这条消息，一看：“哎哟，函数执行失败了，说我传的参数不对”，它会自动在下一轮思考中修正参数再调一次。

### 3. 全局状态机自愈（The Fallback Node Pattern）

这是最高阶的玩法。针对极其复杂的长链路业务，如果节点内部的 try-catch 重试了 3 次还是失败，系统该怎么办？

在企业级 LangGraph 中，我们会画一条专用的“异常流转边（Error Edge）”：

| 组件         | 作用                                                                                                   | Java 对标                       |
| :----------- | :----------------------------------------------------------------------------------------------------- | :------------------------------ |
| **正常流转** | `node_a` -> `node_b`                                                                                   | 正常业务逻辑                    |
| **异常触发** | 如果 `node_a` 多次重试失败，更新 State 中的 `error_flag=True`                                          | `throw new BusinessException()` |
| **路由交警** | 捕获到 `error_flag`，把流程**强行导向** `RecoveryNode`（兜底节点）                                     | 全局 `@ExceptionHandler`        |
| **兜底节点** | `RecoveryNode` 会动用备用方案（比如切换到更聪明的 GPT-4 模型重新梳理上下文），或者降级为“人工介入等待” | 降级策略 / 熔断器               |

## 架构师的防雪崩警告 (The Infinite Loop Trap)

自愈机制虽然强大，但极易引发死循环。如果大模型“轴”上了，它可能会不断输出相同的错误 JSON，你的系统就会无限重试，瞬间把你的 API 额度和 Token 烧光。

铁律：所有的自愈机制，必须设置绝对的 max_retries（最大重试次数，通常设为 2 到 3 次）。一旦达到阈值，必须强制截断并抛出异常。

```py
import os
import json
from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

import env_setup


# 1. 定义增强型状态
class AgentState(TypedDict):
    # add_messages 会让消息不断追加
    messages: Annotated[list, add_messages]
    # 默认覆盖模式：每次更新都会覆盖旧值
    retry_count: int


# 2. 初始化模型
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.7  # 稍微调高，模拟模型可能产生的不确定性
)

MAX_RETRIES = 3


# 3. 节点定义
def agent_node(state: AgentState):
    current_retries = state.get('retry_count', 0)
    print(f"👉 [节点: Agent] 正在思考... (当前尝试次数: {current_retries})")

    # 👿 混沌测试：如果这是第一次请求，直接拦截大模型，强行返回脏数据！
    if current_retries == 0:
        print("   [😈 混沌注入] 拦截 LLM，故意生成包含废话和 Markdown 的脏格式...")
        bad_response = AIMessage(
            content="好的老板！我已经为您处理完毕，以下是您需要的 JSON 结果：\nhttp://googleusercontent.com/immersive_entry_chip/0")
        return {"messages": [bad_response]}

    # 😇 从第二次（即被自愈节点批评后）开始，恢复真正的大模型调用
    sys_msg = SystemMessage(
        content="你是一个严格的 JSON 输出机器。请只回复：{'status': 'success'}。不要带任何 Markdown 标签！"
    )
    return {"messages": [llm.invoke([sys_msg] + state["messages"])]}


def healing_node(state: AgentState):
    current_retries = state.get("retry_count", 0)
    print(f"🛠️ [节点: Self-Healing] 正在准备第 {current_retries + 1} 次纠错指令...")

    # 构造一条强力纠错消息，发给大模型
    error_feedback = HumanMessage(
        content=f"错误：你刚才的回复不符合 JSON 格式！这已经是你第 {current_retries + 1} 次犯错了。请严格检查括号和引号，再试一次！"
    )
    return {
        "messages": [error_feedback],
        "retry_count": current_retries + 1  # 计数器自增
    }


def fail_safe_node(state: AgentState):
    print("🚨 [节点: Fail-Safe] 已达到最大重试次数，系统熔断保护。")
    return {"messages": [AIMessage(content="对不起，我多次尝试修正格式均告失败，已停止重试以保护资源。")]}


# 4. 路由逻辑 (核心控制器)
def router(state: AgentState) -> Literal["heal", "fail_safe", "__end__"]:
    last_msg = state["messages"][-1].content
    current_retries = state.get("retry_count", 0)

    # 模拟校验逻辑：检查是否是合法的 JSON (这里简单演示)
    if last_msg.strip().startswith("{") and last_msg.strip().endswith("}"):
        print("✅ [路由] 格式校验通过，流程结束。")
        return "__end__"

    # 如果格式错误
    if current_retries < MAX_RETRIES:
        print(f"⚠️ [路由] 格式错误，准备回滚自愈 (已试 {current_retries} 次)")
        return "heal"
    else:
        print("🚫 [路由] 错误次数过多，触发熔断。")
        return "fail_safe"


# 5. 编排图网络
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("heal", healing_node)
builder.add_node("fail_safe", fail_safe_node)

builder.add_edge(START, "agent")
# 根据 router 结果决定去向
builder.add_conditional_edges("agent", router)
# heal 完后必须强制回到 agent 让它重新思考
builder.add_edge("heal", "agent")
builder.add_edge("fail_safe", END)

# 编译
memory = MemorySaver()
app = builder.compile(checkpointer=memory)

# 6. 测试运行
config = {"configurable": {"thread_id": "retry_test_001"}}
# 给一个能诱发错误的初始 Prompt
inputs = {"messages": [HumanMessage(content="嘿，帮我写一段话，结尾带个括号。")], "retry_count": 0}

for event in app.stream(inputs, config=config):
    pass
```
