# 一个简单的“查天气”工具

在 Python 的 LangChain 生态里，定义一个提供给大模型的工具，简直和在 Spring Boot 里写一个 `@RestController` 接口一样优雅。大模型本身不会执行代码，它只是极其聪明地帮你组装好了入参（Parameters）。

```py
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

import env_setup


# ==========================================
# 1. 定义本地工具
# ==========================================

# 🌟 @tool 装饰器是核心！它会自动把函数的 docstring 和参数类型声明
# 翻译成大模型认识的 JSON Schema 说明书。
@tool
def get_weather(location: str) -> str:
    """获取指定城市或地区的当前天气情况。"""
    print(f"\n[🖥️ 本地系统执行] 正在调用真实业务接口，查询【{location}】的天气...")
    mock_weather_db = {
        "北京": "晴天，气温 25℃，微风",
        "上海": "雷阵雨，气温 28℃，建议带伞"
    }
    return mock_weather_db.get(location, "未知地区，无法获取天气信息。")


# 准备好我们的工具箱
tools = [get_weather]

# ==========================================
# 2. 初始化大模型并“绑定”工具
# ==========================================

# 注意：务必使用支持 Function Calling 的模型
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",  # 👈 唯一修改的致命一处！
    temperature=0
)

# 🌟 核心动作：把工具的 JSON Schema 说明书“递给”大模型
llm_with_tools = llm.bind_tools(tools)

# ==========================================
# 3. 模拟 Agent 的“三次握手”闭环
# ==========================================
query = "我明天要去上海出差，那边天气怎么样？需要带伞吗？"
print(f"👤 用户提问: {query}")

# 第一步：用户提问
messages = [HumanMessage(content=query)]

print("\n🤖 [LLM 思考中...] ")
# 第一次调用 LLM：它不知道天气，但它知道你有 `get_weather` 这个工具
ai_response = llm_with_tools.invoke(messages)

# 直接将原生的 AI 回复加入对话历史
messages.append(ai_response)

# 第二步：解析并执行
# 检查大模型是不是向我们发起了“函数调用”请求
if ai_response.tool_calls:
    for tool_call in ai_response.tool_calls:
        print(f"📦 [LLM 下发指令] 调用: {tool_call['name']}, 参数: {tool_call['args']}")

        if tool_call["name"] == "get_weather":
            tool_result = get_weather.invoke(tool_call["args"])
            print(f"✅ [本地执行完毕] 获得数据: {tool_result}")

            # 🌟 极其关键：把本地执行的结果，包装成 ToolMessage，按协议扔回给大模型
            tool_msg = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_msg)

# 第三步：带数据做最终请求
print("\n🤖 [LLM 最终总结] 结合本地数据生成回答...")
final_response = llm_with_tools.invoke(messages)

print(f"\n🎉 最终回答:\n{final_response.content}")
```

- 强类型推导（Type Hinting）：注意到 `def get_weather(location: str)` 里的 : str 还有下面的 `"""注释"""` 了吗？如果你不写这些，大模型根本不知道这个函数的参数是什么类型，也不知道这个函数是干嘛的，它就绝对不会去调用。这和后端开发中写 Swagger API 接口文档是完全一样的道理。
- 消息链条（Message Chain）：在传统的聊天里，历史记录只有 `HumanMessage` 和 `AIMessage`。但在 Agent 时代，你的消息链条变成了极其严谨的：`HumanMessage` -> `AIMessage` (附带 tool_calls) -> `ToolMessage` (附带执行结果) -> `AIMessage` (最终自然语言)。少一环，或者 tool_call_id 对不上，大模型就会直接报错。

## 硅基流动 + DeepSeek-V3 的解析大坑

在硅基流动平台上，`deepseek-ai/DeepSeek-V3` 这个模型的 API 封装目前存在一个极其臭名昭著的兼容性问题。它对 LangChain 序列化后的 ToolMessage 格式存在某种极其诡异的洁癖（比如不能包含某些元数据，或者对 tool_call_id 的生成前缀有强制要求）。

在企业级敏捷开发中，遇到这种“由于云厂商底层网关引发的阻塞”，标准的架构师做法是：立刻横向替换一个兼容性极其完美的同级组件，先验证我们自己的业务主链路是否畅通。
