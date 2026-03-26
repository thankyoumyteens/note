# Function Calling

Function Calling（函数调用），是让大模型从“只能陪聊的文科生”进化成“能干实事的工程师”的最核心技术。也可以叫它 Tool Use（工具使用）。

简单来说：大模型本身没有“手”，它不能查数据库、不能调外部 API、不能发邮件。Function Calling 就是你给大模型装上的“手”。

在没有 Function Calling 之前，如果用户问当前的某个指数点位或者最新的市盈率，大模型要么胡编乱造（幻觉），要么抱歉地说“我的知识库只到某年某月”。

## 核心原理：大模型其实是个“包工头”

很多人对 Function Calling 有个巨大的误解，以为是大模型“亲自”去执行了代码。绝对不是！真实的过程是这样的（以查询指数数据为例）：

1. 第一步：递交工具箱（定义 Schema）
   - 你向大模型发送用户的提问时，顺便在 API 请求里带上一个 JSON 格式的“工具说明书”。
   - 比如你告诉它：“我本地有一个函数叫 `get_index_valuation`，需要传入参数 `index_name`，它能返回该指数的最新点位和估值。”
2. 第二步：大模型下达“施工单”
   - 用户提问：“帮我查一下中证人工智能主题指数现在的点位。”
   - 大模型收到后，它的脑子（推理能力）转了一下，发现自己没这数据，但刚好你给的“工具箱”里有 `get_index_valuation`。于是，大模型停止生成废话，而是返回给你一个特殊的结构化 JSON 指令：`{"name": "get_index_valuation", "arguments": "{\"index_name\": \"中证人工智能主题指数\"}"}`
3. 第三步：本地代码执行（你来干活）
   - 你的 Python 或 Java 后端代码拦截到了这个特殊的响应。你的代码解析出函数名和参数，然后由你的服务器去调用真实的本地方法或第三方金融 API，拿到了真实数据：点位 `5566.15`。
4. 第四步：带着结果再次汇报
   - 你把拿到的真实数据 `5566.15` 塞进上下文对话列表里（角色标记为 `tool` 或 `function`），然后再次发起大模型 API 请求。
5. 第五步：大模型润色输出
   - 大模型看到了你塞进来的真实数据，终于有底气了，用自然语言回复用户：“目前中证人工智能主题指数的点位是 5566.15。结合您关注的估值面来看……”

作为习惯了面向对象编程的开发者，你会发现这套架构实现了完美的解耦：

- 大模型只负责“大脑推理”：它从自然语言中精准提取出参数（比如把你随口说的“AI指数”规范化为“中证人工智能主题指数”），决定在什么时候、该用什么工具。
- 你的后端只负责“苦力执行”：数据库账密、API Key、内网权限全都在你自己的服务器上，大模型根本摸不到，保证了绝对的系统安全。

```py
import os

import env_setup

import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)


# ==========================================
# 1. 本地向大模型提供的工具函数
# ==========================================
def get_index_valuation(index_name):
    """这是一个本地函数，模拟去 MySQL 或第三方金融接口查数据"""
    print(f"\n[本地系统日志] 正在执行 SQL 查询 '{index_name}' 的底层数据...")

    # 模拟数据库返回真实数据
    if "人工智能" in index_name or "AI" in index_name.upper():
        # 这里模拟返回极其精确的实时点位和估值
        return json.dumps({
            "index_name": "中证人工智能主题指数",
            "current_point": 5566.15,
            "pe_ratio": 45.2,
            "dividend_yield": 0.5,
            "status": "严重高估"
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "index_name": index_name,
            "current_point": 3500.00,
            "pe_ratio": 12.5,
            "dividend_yield": 3.2,
            "status": "合理偏低"
        }, ensure_ascii=False)


# ==========================================
# 2. 定义递交给大模型的“工具箱” (Schema)
# ==========================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_index_valuation",
            "description": "获取指定股票指数的最新点位、市盈率(P/E)和股息率等估值数据。",
            "parameters": {
                "type": "object",
                "properties": {
                    "index_name": {
                        "type": "string",
                        "description": "指数的官方标准名称，例如：中证人工智能主题指数、沪深300"
                    }
                },
                "required": ["index_name"]
            }
        }
    }
]


def run_trading_agent():
    # 初始对话上下文
    messages = [
        {"role": "system",
         "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你极度看重基本面数据，说话一针见血、极其毒舌。你会使用工具来获取最新数据来支撑你的毒舌言论。"},
        {"role": "user", "content": "帮我看看中证人工智能主题指数现在的点位，你觉得现在能定投吗？"}
    ]

    print("你: 帮我看看中证人工智能主题指数现在的点位，你觉得现在能定投吗？")
    print("-" * 50)

    # ==========================================
    # 第 1 次 API 调用：大模型下达“施工单”
    # ==========================================
    response = client.chat.completions.create(
        model="Pro/moonshotai/Kimi-K2.5",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # 让大模型自己决定用不用工具
    )

    response_message = response.choices[0].message

    # 检查大模型是否决定调用工具
    if response_message.tool_calls:
        # 把大模型“打算调工具”的这个动作，也存入历史记录
        messages.append(response_message)

        # 遍历所有工具调用指令（大模型可能一次性要求调多个工具）
        for tool_call in response_message.tool_calls:
            # 解析出它想调用的函数名和提取出的参数
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"[AI 大脑调度] 大模型决定调用工具: {function_name}")
            print(f"[AI 大脑调度] 提取到的参数: {function_args}")

            # ==========================================
            # 3. 本地代码真正干活
            # ==========================================
            if function_name == "get_index_valuation":
                # 执行本地 Python 函数
                function_response = get_index_valuation(
                    index_name=function_args.get("index_name")
                )

                # ==========================================
                # 4. 把干活的结果汇报给大模型
                # ==========================================
                # 必须使用 'tool' 角色，并带上 tool_call_id，这样大模型才知道这是哪个任务的结果
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

        print("-" * 50)
        # ==========================================
        # 第 2 次 API 调用：大模型拿到数据，润色输出
        # ==========================================
        second_response = client.chat.completions.create(
            model="Pro/moonshotai/Kimi-K2.5",
            messages=messages
        )

        print(f"华尔街老油条: {second_response.choices[0].message.content}")
    else:
        print(f"AI没调用工具，直接输出: {response_message.content}")


if __name__ == "__main__":
    run_trading_agent()
```

## 核心原理解析：Schema 决定一切

在这个机制里，最核心的代码其实是那段 tools 数组配置（JSON Schema）。

这就相当于你在 Java 里定义了一个强类型的 Interface。大模型非常聪明，它不仅会根据你写的 description 来判断什么时候该用这个工具，还会严格按照你规定的 parameters 结构，从用户的自然语言中提取并转换参数。

比如，即使用户随口问的是“AI指数现在多少点”，大模型也会根据上下文，把参数规范化为你要求的“中证人工智能主题指数”，然后再传给你的本地函数。这种“自然语言到结构化参数”的转换能力，就是大模型取代传统正则匹配的最大杀器。
