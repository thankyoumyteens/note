# 滚动总结

强制截断（Buffer Window）虽然解决了性能和 Token 成本问题，但代价是 **“物理性失忆”** ——聊到第 20 轮，AI 就彻底忘了第 1 轮的关键设定。

滚动总结（Summary Memory）完美地平衡了“保留长期记忆”与“控制 Token 消耗”。

架构设计思路

1. 触发机制：每次写 Redis 时检查长度，当 `len(List) >= 20` 时，非阻塞地抛出一个异步任务，主线程立刻向用户返回当前的 AI 回答。
2. 异步总结：后台任务捞出这 20 条消息，用一个专门的“总结 Prompt”请求大模型，要求生成 200 字摘要。
3. 状态替换：将这 20 条长文本从 Redis 中删除，替换为一条 SystemMessage（内容为：“这是之前的对话摘要：...”）。

```py
import os
import json
import asyncio
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# ================= 1. 环境与配置 =================
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

DOUBAO_API_KEY = os.environ.get("OPENAI_API_KEY")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
LLM_ENDPOINT_ID = os.environ.get("ENDPOINT_ID")

if not DOUBAO_API_KEY or not LLM_ENDPOINT_ID:
    raise ValueError("🚨 环境变量缺失，请配置 OPENAI_API_KEY 和 ENDPOINT_ID")

# 初始化 Redis 客户端
# decode_responses=True 会自动将 Redis 的 bytes 解码为 str，省去手动 decode 的麻烦
redis_client = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=True)


# ================= 2. Pydantic 交互模型 =================
class ChatRequest(BaseModel):
    session_id: str = Field(..., description="用户会话ID")
    query: str = Field(..., min_length=1, max_length=1000, description="提问内容")


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    is_summarizing: bool = Field(default=False, description="当前后台是否正在压缩记忆")


# ================= 3. AI 逻辑与异步总结存储引擎 =================
llm = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model=LLM_ENDPOINT_ID,
    temperature=0,
)

# 核心业务 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一位精通金融市场的 AI 投研助手。请用专业、客观、数据驱动的口吻回答用户的投资问题。例如在探讨中证人工智能主题指数时，请精准引用最新点位（如 5566.15点）等关键事实。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# 专门用于生成摘要的内部 Prompt
SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个对话总结助手。请将以下对话历史浓缩成一段不超过 200 字的摘要，务必保留其中的关键事实（如提到的特定股票、财务指标）和核心上下文。"),
    ("human", "{chat_history}")
])


class SummarySingleRedisHistory(BaseChatMessageHistory):
    """Redis 版的滚动总结功能实现"""

    def __init__(self, session_id: str, threshold: int = 10, ttl: int = 604800):
        self.session_id = session_id
        self.key_prefix = "ai_agent:chat_summary:"
        self.threshold = threshold
        self.ttl = ttl
        self.is_summarizing = False

    @property
    def key(self) -> str:
        return self.key_prefix + self.session_id

    @property
    def messages(self) -> List[BaseMessage]:
        _items = redis_client.lrange(self.key, 0, -1)
        # 因为 redis_client 开启了 decode_responses，取出来的直接是 str
        items = [json.loads(m) for m in _items[::-1]]
        return messages_from_dict(items)

    def add_message(self, message: BaseMessage) -> None:
        # 1. 正常追加消息
        redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
        if self.ttl:
            redis_client.expire(self.key, self.ttl)

        # 2. 检查阈值，触发旁路任务
        current_length = redis_client.llen(self.key)
        if current_length >= self.threshold and not self.is_summarizing:
            self.is_summarizing = True
            # 将异步总结任务抛入 Uvicorn 的事件循环中，不阻塞当前 HTTP 响应
            asyncio.create_task(self._async_summarize())

    async def aadd_messages(self, messages: List[BaseMessage]) -> None:
        """
        重写原生的异步添加方法。
        LangChain 的 ainvoke 会优先调用此方法，确保代码运行在 Uvicorn 的主事件循环中。
        """
        # 1. 批量存入新消息
        for message in messages:
            redis_client.lpush(self.key, json.dumps(message_to_dict(message)))

        if self.ttl:
            redis_client.expire(self.key, self.ttl)

        # 2. 检查长度并触发异步总结
        current_length = redis_client.llen(self.key)

        if current_length >= self.threshold and not self.is_summarizing:
            self.is_summarizing = True
            # 因为明确身处主事件循环中，这里的 create_task 完全合法且安全
            asyncio.create_task(self._async_summarize())

    async def _async_summarize(self):
        try:
            print(f"\n[后台任务] 检测到对话超过 {self.threshold} 条，触发记忆总结 (Session: {self.session_id})...")
            current_messages = self.messages
            history_text = "\n".join([f"{m.type}: {m.content}" for m in current_messages])

            summary_chain = SUMMARY_PROMPT | llm
            # ainvoke 异步调用大模型，释放 CPU
            summary_response = await summary_chain.ainvoke({"chat_history": history_text})
            summary_text = summary_response.content

            print(f"[后台任务] 摘要生成完成: {summary_text[:50]}...")

            new_memory = SystemMessage(content=f"之前的对话摘要：{summary_text}")

            # 原子化替换：先删后插
            pipeline = redis_client.pipeline()
            pipeline.delete(self.key)
            pipeline.lpush(self.key, json.dumps(message_to_dict(new_memory)))
            pipeline.execute()

            print(f"[后台任务] Redis 状态已更新。记忆已压缩为 1 条摘要。")
        except Exception as e:
            print(f"[后台任务] 总结失败: {e}")
        finally:
            self.is_summarizing = False

    def clear(self) -> None:
        redis_client.delete(self.key)


# 全局状态字典，用于在单例运行期间保持引用，防止垃圾回收导致状态锁丢失
history_store = {}


def get_summary_redis_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in history_store:
        # 这里将阈值设为 4 条（即 2 轮对话），方便你快速测试出总结效果
        history_store[session_id] = SummarySingleRedisHistory(session_id=session_id, threshold=4)
    return history_store[session_id]


chain = prompt | llm

conversational_chain = RunnableWithMessageHistory(
    chain,
    get_summary_redis_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

# ================= 4. FastAPI 路由 =================
app = FastAPI(title="投研 AI 滚动总结 API")


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 获取大模型回答
        response = await conversational_chain.ainvoke(
            {"question": request.query},
            config={"configurable": {"session_id": request.session_id}}
        )

        # 探查一下后台任务状态，返回给调用方做状态指示
        history_instance = history_store.get(request.session_id)
        is_summarizing = history_instance.is_summarizing if history_instance else False

        return ChatResponse(
            session_id=request.session_id,
            reply=response.content,
            is_summarizing=is_summarizing
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务异常: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

1. 打开 Swagger UI：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. 因为代码里我将 threshold 故意设为了 4（一问一答算2条，即2轮对话后就会触发总结），你可以连续发起三次请求来观察控制台日志：
   1. 请求 1："我现在考虑投资美股，但 TSLA 波动太大了。"
   2. 请求 2："你觉得用博格公式来评估它合理吗？" -> 此时达到 4 条记录，API 返回后，你会立刻在 Pycharm 控制台看到后台触发了摘要生成。
   3. 请求 3："那我之前考虑的是哪家公司？" -> 大模型会准确回答出 TSLA，此时你可以用 redis-cli 连上本地看看，原本冗长的对话数组已经被替换成了一条精简的 SystemMessage。
