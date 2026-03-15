# 构建带有记忆的终端对话机器人

在最新版的 LangChain 中，我们通常使用 RunnableWithMessageHistory 来优雅地包裹我们在第四步学到的 LCEL Chain。它能拦截你的输入，自动从存储（比如 Redis 或数据库）中抓取历史记录拼接到 Prompt 里，再把大模型的新回答写回存储中。

### 1. 安装依赖

```sh
pip install langchain langchain-openai redis langchain-community
```

### 2. redis_memory.py

```py
import os

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 强行清理可能存在的代理环境变量，确保直连国内 API
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

# ================= 豆包 (Volcengine) 配置区 =================
DOUBAO_API_KEY = os.environ.get("OPENAI_API_KEY")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
LLM_ENDPOINT_ID = os.environ.get("ENDPOINT_ID")  # 对话模型接入点id
# =========================================================

REDIS_URL = "redis://localhost:6379/0"

# 1. 初始化模型
llm = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model=LLM_ENDPOINT_ID,
    temperature=0,
)

# 2. 构建 Prompt 模板
# 注意这里的 MessagesPlaceholder，它就像一个占位符“管道”，专门用来动态灌入历史消息
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位资深的金融数据工程师，擅长处理美股市场的数据清洗与架构设计。请用专业、干练的口吻回答。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# 3. 构建基础的 LCEL Chain
chain = prompt | llm


# 4. 定义一个工厂函数，返回 RedisChatMessageHistory 实例
def get_redis_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        key_prefix="chat_memory:"  # 规范的 Redis Key 前缀，方便管理
    )


# 5. 包装 Chain
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_redis_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

# ================= 测试对话 =================
if __name__ == "__main__":
    print("🤖 接入 Redis 的金融数据助手已启动...\n" + "-" * 40)

    # 我们硬编码一个 session_id 模拟同一个用户的连续会话
    config = {"configurable": {"session_id": "investor_session_tsla_001"}}

    # 第一轮：提出问题
    q1 = "TSLA 目前的股价数据可能不准，你能告诉我处理这种脏数据的常规工程手段吗？"
    print(f"\n👨‍💻 用户: {q1}")
    response1 = conversational_chain.invoke({"question": q1}, config=config)
    print(f"🤖 AI: {response1.content}")

    # 第二轮：追问上下文
    q2 = "那么在这个过程中，Redis 可以用来做什么？"
    print(f"\n👨‍💻 用户: {q2}")
    response2 = conversational_chain.invoke({"question": q2}, config=config)
    print(f"🤖 AI: {response2.content}")
```

## 使用 Redis Cluster

LangChain 的 RedisChatMessageHistory 如果只接收一个 `url="redis://..."` 参数，它底层默认实例化的是单机的 redis.Redis 客户端。面对集群，它会直接报错。

我们不让 LangChain 去创建连接，而是我们自己使用 Python 的 redis 库创建一个正宗的 RedisCluster 客户端，然后把它注入到 LangChain 的配置中。

```py
from redis.cluster import RedisCluster
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. 手动初始化 Redis Cluster 客户端 (这里以三个启动节点为例)
# 这就相当于你在 Spring Boot 里的 spring.redis.cluster.nodes 配置
cluster_client = RedisCluster(
    startup_nodes=[
        {"host": "10.0.0.1", "port": "7000"},
        {"host": "10.0.0.2", "port": "7000"},
        {"host": "10.0.0.3", "port": "7000"},
    ],
    password="your_password",  # 如果有密码的话
    decode_responses=True      # 建议开启，直接处理字符串而不是 bytes
)

# 或者，如果你有统一的集群入口 URL (需要 redis-py 4.2+ 支持)
# cluster_client = RedisCluster.from_url("redis://10.0.0.1:7000")

# 2. 修改你的工厂函数
def get_redis_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        redis_client=cluster_client,  # <--- 核心改变：弃用 url，直接注入集群客户端实例
        key_prefix="chat_memory:"
    )

# 后面的包装逻辑完全不需要改动
conversational_chain = RunnableWithMessageHistory(
    chain,
    get_redis_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)
```
