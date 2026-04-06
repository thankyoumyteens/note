# SystemMessage、HumanMessage、AIMessage和ToolMessage

这三个概念不仅是 LangChain 的基础，更是整个现代大模型（LLM）API 通信协议的底层基石。

在 2022 年 ChatGPT 诞生之前，我们调用大模型（比如 GPT-3）使用的是纯文本拼接协议（Text Completion）。也就是把所有指令、历史记录揉成一个长长的 String 发过去。

但 OpenAI 发现，如果把设定和用户的提问混在一起，大模型经常分不清到底该听谁的（极易发生 Prompt 注入）。于是，他们发明了 Chat Completion 协议。

在这个协议中，发给大模型的不再是一个长字符串，而是一个结构化的 JSON 数组（List of Dicts）。每一条消息都必须带有一个明确的 role（角色） 标签。

这三个类，就是 LangChain 对底层协议角色的面向对象封装：

- SystemMessage（底层 Role: system）
  - 大白话：“上帝视角的系统设定” / “Root 权限指令”
  - 作用：它是全局的背景音，用来定义大模型的人设、语气、底线规则、输出格式。
  - 架构师视角：普通用户（C端）在界面上是绝对看不到、也无法修改这条消息的。在注意力机制（Attention）的计算权重上，现代大模型通常会赋予 system 消息最高的优先级。
  - 举例：`SystemMessage(content="你是一个精通 Java 的架构师，只能用中文回答，绝不能输出 Markdown 以外的格式。")`
- HumanMessage（底层 Role: user）
  - 大白话：“真实用户的输入”
  - 作用：代表正在屏幕前敲字的那个人的提问、指令或者上传的图片。
  - 架构师视角：这是“不可信数据”。大模型在阅读 user 消息时，会保持警惕，如果 user 让你“忽略之前的设定”，大模型会对比 system 消息并拒绝执行。
  - 举例：`HumanMessage(content="帮我写一个快速排序算法。")`
- AIMessage（底层 Role: assistant）
  - 大白话：“大模型自己的回复”
  - 作用：记录大模型之前说过的话，用于拼接多轮对话历史，让大模型拥有上下文记忆。
  - 架构师视角（极其关键）：在 Agent 架构中，AIMessage 不仅能携带文本（大模型说的话），它还是唯一能携带 tool_calls（调用工具指令） 的消息载体。
  - 举例：`AIMessage(content="好的，这是为你编写的快速排序算法：...")`
- ToolMessage（底层 Role: tool）
  - 大白话：“系统工具的真实执行汇报单”
  - 作用：当大模型发起工具调用指令后，用来承载你在本地物理服务器上运行代码（如查外部 API、读本地数据库）所获取的真实数据，并将这些数据喂给大模型，作为它进行下一步总结或决策的事实依据。
  - 架构师视角（极其关键）：它与 AIMessage 之间存在着极其严格的因果与时序绑定。在底层 HTTP 请求中，一条 ToolMessage 必须紧跟在那个包含 tool_calls 的 AIMessage 之后，并且必须强制携带 tool_call_id（这就相当于分布式追踪链路里的 Trace ID 回调）。如果 ID 对应不上或者顺序错乱，底层 API 网关会瞬间抛出 400 Bad Request 异常。它是打破大模型信息孤岛的唯一“合法货车”。
  - 举例：`ToolMessage(content="上海明天雷阵雨，气温 28℃", tool_call_id="call_xyz789", name="get_weather")`

在真正的 Agent 流转中，当大模型决定查天气时，Python 内存里的状态流转（State）长这个样子：

```py
messages = [
    SystemMessage(content="你是天气助手。"),
    HumanMessage(content="上海天气如何？"),

    # 大模型此时并未输出自然语言，而是输出了一段特殊的“函数调用指令”
    AIMessage(
        content="",
        tool_calls=[{"name": "get_weather", "args": {"city": "上海"}, "id": "call_abc123"}]
    ),

    # 本地（ToolNode）执行完函数后，强制追加一条带有对应 ID 的 ToolMessage
    ToolMessage(
        content="上海今天雷阵雨，28℃",
        tool_call_id="call_abc123"
    )
]
```

当这段代码被触发（invoke）时，LangChain 会将其序列化。你在底层抓包看到的、发给 OpenAI 服务器的真实 JSON 长这样：

```json
"messages": [
  {
    "role": "system",
    "content": "你是天气助手。"
  },
  {
    "role": "user",
    "content": "上海天气如何？"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"city\": \"上海\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "上海今天雷阵雨，28℃"
  }
]
```

当包含这 4 条消息的 JSON 发给大模型后，大模型看到最后一条是 tool 传回来的真实气温，它才会生成第 5 条消息（一个新的 `{"role": "assistant", "content": "上海今天是雷阵雨，气温28℃，出门记得带伞哦！"}`）返回给用户。

剥开所有 Python 的面向对象糖衣，大模型的所谓“智能行动”，本质上就是在这条高度结构化的 JSON 数组上，进行着极度严谨的“接龙游戏”。

## 退役的 ChatPromptTemplate 代码

```py
qa_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一位精通金融市场和公司制度的 AI 投研助手。\n"
     "请务必结合用户过往的对话历史，并根据下方提供的【参考资料】进行严谨、专业、数据驱动的回答。\n"
     "如果参考资料中没有提到相关信息，请诚实回答不知道，严禁凭空编造事实。\n\n"
     "【参考资料】：\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])
```

这种写法在真正的 Agent 架构里，基本可以宣告光荣退役了。

作为一名 Java 后端开发者，你可以这样理解这种变迁：

这段 ChatPromptTemplate 代码，就像是传统的 JSP。你必须提前把坑位（`{context}` 和 `{chat_history}`）挖好，然后在请求发出的那一瞬间，把所有数据一股脑地塞进模板里拼成一个大字符串。

而在 LangGraph 的 Agent 架构中，大模型通信变成了现代的 RESTful API + JSON 状态流转模式。

我们来看看为什么这三个“坑位”都不需要了：

1. `{context}` 去哪了？
   - 过去（填空题）：你必须先通过外挂的向量数据库查到文本，强行拼接到 System Prompt 里的 `{context}` 处，再喂给大模型。大模型是被动接收的。
   - 现在（动态消息）：大模型变成了主动方。它觉得需要资料，就自己去调 `search_company_knowledge_base` 工具。工具执行完后，会返回一个 ToolMessage 附加在对话流的末尾。大模型自己会去阅读这个 ToolMessage 获取上下文。我们彻底消灭了繁琐的字符串拼接。
2. `MessagesPlaceholder("chat_history")` 去哪了？
   - 过去（外挂拦截）：因为底层的 Runnable 链条没有记忆，你需要用这个 Placeholder 配合 RunnableWithMessageHistory，像 AOP 拦截器一样在每次请求前去 Redis 里把历史记录扒出来塞进去。
   - 现在（原生状态）：LangGraph 的 State（也就是 MessagesState）本身就是一个原生的消息数组。历史记录天然就在状态机里流转，不需要任何占位符。
3. `{question}` 去哪了？
   - 过去：强行把用户的输入包装成一句话。
   - 现在：用户的提问在最开始点火时，就已经作为一个标准的 HumanMessage 存入了 `state["messages"]`。

## 代码的极致进化（Before vs. After）

在 Agent 时代，我们只保留最纯粹的 System Prompt（人设与规则），剩下的全靠状态机流转。

❌ 过去的臃肿链条 (LCEL)

```py
# 还要写一个专门格式化 Document 的函数
def format_docs(docs): ...

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | qa_prompt
    | llm
)
```

✅ 现在的极简节点 (LangGraph Node)

```py
def call_model(state: MessagesState):
    # 1. 定义纯粹的人设（不需要挖任何变量坑位）
    sys_msg = SystemMessage(content="你是精通金融的 AI 投研助手。绝不凭空捏造。")

    # 2. 把人设放在当前所有历史消息的最前面
    messages = [sys_msg] + state["messages"]

    # 3. 直接调用！历史记录和 Tool 返回的 Context 全都在 messages 数组里
    response = llm.invoke(messages)

    return {"messages": [response]}
```

正是因为抛弃了那种死板的模板绑定，你的 Agent 才获得了极其强大的灵活性：它可以在同一轮对话里，先扮演研究员查资料，再扮演撰稿人写文章。如果把它焊死在 Prompt 模板里，这种多角色动态流转是根本做不到的。
