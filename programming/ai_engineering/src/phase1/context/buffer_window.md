# 强制截断

在传统的后端架构中，如果一个 List 无限增长，你的第一反应肯定是 OOM（内存溢出）或者网络 I/O 阻塞。在 AI 应用里，不仅会引发这两点，更会直接导致 API Token 费用失控和响应延迟剧增。

实现强制截断（Buffer Window），在工程上有两个层面的做法。

## 方案一：应用层截断 (通过 LCEL 管道拦截)

LangChain 官方提供了一个非常强大的工具 trim_messages。它的优雅之处在于，它不仅能按数量截取，还能保证消息对的完整性（比如强行截断后，保证第一条依然是 User 发出的，而不是 AI 的半截废话）。

我们利用 RunnablePassthrough，在历史记录流向 Prompt 之前，像加一个 Filter 一样把它“砍”掉一半。

```py
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnablePassthrough

# ... (前面初始化 llm 和 RedisCluster 的代码保持不变) ...

# 1. 定义截断器 (Trimmer)
trimmer = trim_messages(
    max_tokens=10,          # 这里指保留最后 10 条消息（即 5 轮对话）
    strategy="last",        # 保留尾部（最新）的消息
    token_counter=len,      # 计数策略：直接按 List 里的对象数量算
    include_system=True,    # 核心！System Prompt 绝对不能被截掉
    start_on="human"        # 强校验：截断后的对话起点必须是用户的提问，防止逻辑断层
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位资深的金融数据工程师..."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# 2. 核心改变：在数据流入 prompt 之前，强行覆盖 chat_history 变量
# RunnablePassthrough.assign 会获取传入的字典，并将 chat_history 字段替换为截断后的结果
chain = (
    RunnablePassthrough.assign(chat_history=lambda x: trimmer.invoke(x["chat_history"]))
    | prompt
    | llm
)

# 3. 包装机制不变
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_redis_history, # 你的 Redis Cluster 工厂函数
    input_messages_key="question",
    history_messages_key="chat_history"
)
```

当请求进来时，RunnableWithMessageHistory 会从 Redis 里把（假设已经积攒了 100 条的）历史记录全捞出来，放进名为 chat_history 的变量。接着，数据流到了 RunnablePassthrough，trimmer 咔嚓一刀，只剩下最后 10 条，最后这 10 条才会被填入 MessagesPlaceholder 发给大模型。

## 方案二：持久层截断 (Redis LTRIM，更硬核的后端解法)

虽然方案一代码很优雅，但你从系统底层的角度审视一下，就会发现一个巨大的性能黑洞：

如果用户聊了 10,000 轮，方案一是把这 10,000 条记录全从 Redis 拉到 Python 进程的内存里，然后再切出最后 10 条。这白白浪费了极大的网络带宽和反序列化开销。

真正的企业级做法，是在写入 Redis 时就控制住列表的长度，就像我们在处理热点数据队列时常用的手段。

LangChain 允许你继承并重写底层的存储逻辑。我们可以自己封装一个带有 LTRIM 机制的 Redis History：

```py
from langchain_community.chat_message_histories import RedisChatMessageHistory

class BoundedRedisChatMessageHistory(RedisChatMessageHistory):
    """
    自定义的 Redis 历史存储类，支持容量上限限制。
    """

    def __init__(self, session_id: str, url, key_prefix: str = "chat_memory:", max_size: int = 10):
        super().__init__(session_id=session_id, url=url, key_prefix=key_prefix)
        self.max_size = max_size

    def add_message(self, message) -> None:
        # 1. 先调用父类方法，正常把消息追加进 Redis (内部调用了 RPUSH)
        super().add_message(message)

        # 2. 追加完成后，立即触发 LTRIM，只保留最后 N 条记录
        # LTRIM key -max_size -1 表示保留倒数 max_size 个元素到最后一个元素
        if self.max_size > 0:
            self.redis_client.ltrim(self.key, -self.max_size, -1)
```

只需要把你的工厂函数替换成这个新类即可：

```py
def get_bounded_redis_history(session_id: str):
    return BoundedRedisChatMessageHistory(
        session_id=session_id,
        redis_client=cluster_client, # 你的 RedisCluster 实例
        key_prefix="chat_memory:",
        max_size=10 # 强制 Redis 里最多只存 10 条
    )

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_bounded_redis_history,
    # ...
)
```

采用方案二后，你的 Redis List 永远不会超过 10 条（大约几 KB）。每次 HTTP 请求拉取的网络 I/O 被严格限制在了 O(1) 的常数级别，哪怕面对极高并发的对话请求，你的 Python 服务和 Redis 集群也能稳如泰山。
