# 给大模型加上联网功能

作为习惯了通过接口调用外部服务的 Java 开发者，你完全可以把“搜索引擎”看作是一个巨大的第三方 RESTful API。大模型负责提取你想搜的关键词（Query），我们的 Python 代码负责去调用搜索引擎获取网页摘要，最后再喂给大模型做总结。

为了让你无需繁琐地去申请 Google 或 Bing 的 API Key，我们将使用业界极其良心的开源库 duckduckgo-search（它完全免费，且不需要任何 Key）。

### 1. 安装依赖

```sh
pip install ddgs
```

### 2. 代码

```py
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from ddgs import DDGS

import env_setup


# ==========================================
# 1. 定义极其硬核的“联网搜索”工具
# ==========================================
@tool
def search_web(query: str) -> str:
    """
    当需要获取实时信息、最新新闻、或者你不知道的客观事实时，调用此工具。
    输入参数为你要在搜索引擎中输入的精准关键词。
    """
    print(f"\n[🌐 突破次元壁] 正在直连互联网，全网检索关键词：【{query}】...")

    try:
        # 实例化 DuckDuckGo 搜索客户端
        ddgs = DDGS()
        # 搜索并获取前 3 条最相关的网页摘要
        results = ddgs.text(query, max_results=3)

        if not results:
            return "未在互联网上检索到相关信息。"

        # 将搜索到的网页标题和摘要拼接成一段纯文本，供大模型阅读
        formatted_results = "\n".join(
            [f"标题: {res['title']}\n摘要: {res['body']}" for res in results]
        )
        return formatted_results

    except Exception as e:
        return f"搜索失败，网络异常或接口报错: {str(e)}"


# 将我们的联网大炮装载进工具箱
tools = [search_web]

# ==========================================
# 2. 初始化大模型并挂载工具
# ==========================================
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",  # 极其稳定的底座
    temperature=0.1
)
llm_with_tools = llm.bind_tools(tools)

# ==========================================
# 3. 见证奇迹：让模型去查一件它绝对不可能知道的事
# ==========================================
# 你可以随便问一个极其晚近的新闻，或者今天实时的金融数据
query = "帮我查一下，SpaceX 星舰最新的试飞情况如何？发射成功了吗？"
print(f"👤 用户提问: {query}")

messages = [HumanMessage(content=query)]

print("\n🤖 [LLM 思考中...] 分析发现自己的知识库已过期，必须向互联网求助...")
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

# 【解析指令并执行真正的网络搜索】
if ai_response.tool_calls:
    for tool_call in ai_response.tool_calls:
        print(f"📦 [LLM 下发指令] 动用搜索工具: {tool_call['name']}, 搜索词: {tool_call['args']}")

        if tool_call["name"] == "search_web":
            # 真实发起 HTTP 请求，爬取全网最新数据
            tool_result = search_web.invoke(tool_call["args"])
            print(f"✅ [爬取完毕] 获得最新网页摘要，即将投喂给大模型整理...")

            # 标准协议封装回传
            tool_msg = ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_msg)

# 【带着全网最新鲜的知识进行最终生成】
print("\n🤖 [LLM 最终总结] 正在疯狂阅读网页摘要，为你生成最终简报...")
final_response = llm_with_tools.invoke(messages)

print(f"\n🎉 终极回答:\n{final_response.content}")
```
