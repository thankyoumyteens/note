# MessagesState

MessagesState 是 LangGraph 官方为你提前写好的一个 “内置标准模板”。

在咱们前几步的实战中，为了让你看懂底层原理，我带你手写了这样一个状态类：

```py
class TeamState(TypedDict):
    messages: Annotated[list, add_messages]
    ...
```

LangGraph 的作者们发现，全网 99% 的大模型图编排应用，底层都必定需要一个包含 messages 字段的对话历史数组，而且追加逻辑也全都是 `add_messages`。

既然大家都这么写，官方干脆把它封装进了源码里，命名为 MessagesState。

如果你在 PyCharm 里按住 Ctrl / Cmd 键点击 MessagesState 看它的底层源码，你会发现它简单得令人发指：

```py
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

## 如何基于它扩展业务字段？

在真实的企业级业务中，光传递消息肯定不够。你可能还需要在节点之间传递用户的 userId、查到的 documents、或者风控的 risk_score。

在 Python 里，你可以极其优雅地继承 MessagesState 并扩展它：

```py
from langgraph.graph import MessagesState

# 继承官方的基类，自带了 messages 字段
class EnterpriseState(MessagesState):
    user_id: str             # 额外传递当前操作人的 ID
    documents: list[str]     # 额外传递 RAG 检索出来的文档
    is_vip: bool             # 额外传递业务标记
```

这样，你的 EnterpriseState 既拥有了自动追加对话历史的超能力，又装载了你专属的业务数据，这才是企业级图编排的最终形态！
