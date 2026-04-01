# 把 RAG 封装成 Tool

在阶段二（RAG 阶段）时，我们系统的入口是直接对着 RAG 发起的。用户的每次提问，系统都会死板地走一遍：向量检索 -> Redis 回表 -> 重排 -> 给大模型生成。

这在 Java 后端开发中，就像是一段写死在 `main()` 方法里的线性脚本，毫无弹性。

但到了阶段三（Agent 阶段），范式彻底改变了！RAG 不再是系统的“主干（Main Pipeline）”，它被降维了！它变成了 Agent 武器库（Tools）里的其中一把武器。

Agent 变成了类似 Spring MVC 里的 DispatcherServlet。当用户提问时：

1. Agent 先思考：这个问题属于公司内部制度吗？
2. 如果是，它就拔出 RAG 检索工具。
3. 如果问的是最新的马斯克星舰发射，它就拔出 DuckDuckGo 联网工具。
4. 如果问的是“1+1等于几”，它什么工具都不拔，直接跟你聊天。

还记得你在阶段二写的那个极其硬核的 ultimate_retriever（包含 Qdrant、Redis、硅基流动重排）吗？

现在，我们要用一个 @tool 装饰器，把这台 V8 引擎直接包裹起来，递给大模型。

你可以新建一个 agent_with_rag.py，直接运行这段代码感受一下这种多路由动态分发的恐怖威力：

```py
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

import env_setup


# 🌟 1. 导入你阶段二写好的 RAG 检索器
# (假设你把阶段二的检索器初始化代码封装在了一个文件 rag_engine.py 里)
# from rag_engine import ultimate_retriever

# 为了演示，这里我们 mock 一下那个 ultimate_retriever 的返回结果
class MockRetriever:
    def invoke(self, query):
        from langchain_core.documents import Document
        if "请假" in query:
            return [Document(page_content="内部员工请假需提前1天在考勤系统提交申请，3天以上需总监审批。",
                             metadata={"source": "HR手册"})]
        return []


ultimate_retriever = MockRetriever()


# ==========================================
# 工具 1：内部知识库 (你的 RAG 系统)
# ==========================================
@tool
def search_company_knowledge_base(query: str) -> str:
    """
    当用户询问公司内部制度、员工手册、请假流程、IT规范、报销流程等【内部知识】时，必须调用此工具。
    输入参数为您提取的精简检索关键词。
    """
    print(f"\n[🗄️ 触发 RAG 引擎] 正在潜入公司内部 Qdrant+Redis 知识库，检索关键词：【{query}】...")

    # 直接调用你阶段二写好的终极大炮！
    docs = ultimate_retriever.invoke(query)

    if not docs:
        return "内部知识库中未找到相关规定。"

    # 把检索到的 Document 对象格式化成字符串，喂给 Agent
    return "\n\n".join([f"【来源】: {doc.metadata}\n【内容】: {doc.page_content}" for doc in docs])


# ==========================================
# 工具 2：全网实时搜索 (上一步写的鸭鸭杀)
# ==========================================
@tool
def search_web(query: str) -> str:
    """
    当用户询问外部实时新闻、最新金融数据、或公众人物事件时，调用此工具去互联网查找。
    """
    print(f"\n[🌐 触发联网引擎] 正在直连互联网，全网检索关键词：【{query}】...")
    from ddgs import DDGS
    try:
        results = DDGS().text(query, max_results=2)
        return "\n".join([f"摘要: {res['body']}" for res in results]) if results else "未找到外部信息。"
    except Exception as e:
        return f"外网搜索失败: {e}"


# 🌟 将两把绝世武器装入工具箱
tools = [search_company_knowledge_base, search_web]

# ==========================================
# 核心 Agent 运行逻辑
# ==========================================
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.1
)
llm_with_tools = llm.bind_tools(tools)

# 🧪 测试场景：你可以切换下面这两个 query，看看 Agent 的动态路由到底有多聪明！
# query = "帮我查一下外网，SpaceX 最新发射成功了吗？"
query = "我生病了没法提前请假，流程怎么走？"

print(f"👤 用户提问: {query}")
messages = [HumanMessage(content=query)]
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

if ai_response.tool_calls:
    for tool_call in ai_response.tool_calls:
        print(f"📦 [LLM 路由决策] 决定动用武器: {tool_call['name']}, 提取入参: {tool_call['args']}")

        # 动态分发！
        if tool_call["name"] == "search_company_knowledge_base":
            tool_result = search_company_knowledge_base.invoke(tool_call["args"])
        elif tool_call["name"] == "search_web":
            tool_result = search_web.invoke(tool_call["args"])

        print(f"✅ [武器执行完毕] 获取情报成功，准备生成最终简报...")

        tool_msg = ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"], name=tool_call["name"])
        messages.append(tool_msg)

    final_response = llm_with_tools.invoke(messages)
    print(f"\n🎉 终极回答:\n{final_response.content}")
else:
    print(f"\n🎉 AI 认为无需调用工具，直接回答:\n{ai_response.content}")
```

这就是真正的智能体（Agent）！ RAG 只是它右兜里的一个记事本，鸭鸭杀是它左兜里的一个手机。它有足够的智商去判断，什么时候该看记事本，什么时候该看手机。
