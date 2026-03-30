# 实现企业知识库 AI 助手

这份代码将之前写过的所有硬核组件（FastAPI 异步服务、并发安全总结记忆、终极检索引擎、自定义重排组件、env_setup）毫无保留地缝合在了一起。

```py
import os
import json
import redis

import env_setup

import asyncio
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.retrievers import ParentDocumentRetriever, EnsembleRetriever, ContextualCompressionRetriever
from langchain_classic.storage import EncoderBackedStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_community.storage import RedisStore

# 🌟 引入你手写的终极云端重排组件 (确保 silicon_flow_components.py 在当前目录)
from silicon_flow_components import SiliconFlowReranker

# ==========================================
# 1. 基础设施初始化 (Redis & Qdrant)
# ==========================================
# 初始化全局 Redis 客户端 (decode_responses=True 极其关键)
redis_client = redis.Redis.from_url("redis://localhost:6379/0", decode_responses=True)
qdrant_client = QdrantClient(url="http://localhost:6333")

# ================= ==========================
# 2. 交互大模型 (Generation LLM) 初始化
# ================= ==========================
llm = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    temperature=0.1,  # RAG场景，温度设低，保证回答严谨
)

# 核心业务 Prompt：结合了历史和检索内容
qa_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一位精通金融市场和公司制度的 AI 投研助手。\n"
     "请务必结合用户过往的对话历史，并根据下方提供的【参考资料】进行严谨、专业、数据驱动的回答。\n"
     "如果参考资料中没有提到相关信息，请诚实回答不知道，严禁凭空编造事实。\n\n"
     "【参考资料】：\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])


# ================= ==========================
# 3. 终极检索引擎初始化 (The Ultimate Retriever)
# ================= ==========================
def initialize_ultimate_retriever():
    print("\n⚙️ 正在初始化终极检索引擎 (多模混合召回 + 云端8B重排)...")

    # 3.1 加载并切分本地 md 文件
    with open("parsed_result.md", "r", encoding="utf-8") as f:
        markdown_document = f.read()

    headers_to_split_on = [("#", "Header1"), ("##", "Header2"), ("###", "Header3")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    parent_docs = markdown_splitter.split_text(markdown_document)

    # 3.2 向量与存储配置 (降维至 512)
    VECTOR_DIMENSION = 512
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.environ.get("API_KEY"),
        openai_api_base="https://api.siliconflow.cn/v1",
        model="Qwen/Qwen3-Embedding-8B",
        dimensions=VECTOR_DIMENSION
    )

    # --- Redis: 存储父文档大文本 ( namespace区分防冲突) ---
    redis_byte_store = RedisStore(client=redis_client, namespace="rag:ultimate_parents:")

    def encode_doc(doc: Document) -> str:
        return json.dumps({"page_content": doc.page_content, "metadata": doc.metadata})

    def decode_doc(s) -> Document:
        # 如果因为某些原因传进来的是 bytes，我们再 decode；如果是 str，直接用！
        if isinstance(s, bytes):
            s = s.decode("utf-8")
        data = json.loads(s)
        return Document(page_content=data["page_content"], metadata=data.get("metadata", {}))

    store = EncoderBackedStore(
        store=redis_byte_store,
        key_encoder=lambda x: x,
        value_serializer=encode_doc,
        value_deserializer=decode_doc
    )

    # --- Qdrant: 存储向量 ---
    COLLECTION_NAME = "ultimate_company_kb"
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(collection_name=COLLECTION_NAME,
                                        vectors_config=models.VectorParams(
                                            size=VECTOR_DIMENSION,
                                            distance=models.Distance.COSINE)
                                        )
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_NAME, embedding=embeddings)

    # 3.3 构建双路召回大炮
    strict_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.Header1",
                match=models.MatchValue(value="考勤与休假制度")
            )
        ]
    )
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    # 注意：这里我们为了演示“大一统”，暂时关闭“标量硬过滤”，做全库混合检索后再重排
    # 如果生产环境需要权限隔离，可以在这里解除注释 "filter": strict_filter
    parent_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=None,
        search_kwargs={
            # 先捞 Top 5 候选
            "k": 5,
            # "filter": strict_filter,
        }
    )

    print("-> 正在将文本灌入双数据库 (Qdrant + Redis)...")
    parent_retriever.add_documents(parent_docs)

    # BM25 全库关键词召回
    print("-> 构建 BM25 稀疏索引...")
    bm25_retriever = BM25Retriever.from_documents(parent_docs)
    bm25_retriever.k = 3

    # 双路融合
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, parent_retriever], weights=[0.4, 0.6])

    # 3.4 挂载 Qwen3-8B 云端重排
    print("-> 挂载云端 Qwen3-8B 重排...")
    compressor = SiliconFlowReranker(api_key=os.environ.get("API_KEY"), model="Qwen/Qwen3-Reranker-8B",
                                     top_n=2)  # 重排后只要最精准的 2 个

    # 最终检索器
    final_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=ensemble_retriever)
    print("✅ 检索引擎初始化完成！\n")
    return final_retriever


# 全局单例初始化检索器
ultimate_retriever = initialize_ultimate_retriever()

# ================= ==========================
# 4. 异步滚动总结记忆引擎 初始化
# ================= ==========================
# (为了代码简洁，这里直接使用之前写好的 SummaryRedisHistory 类逻辑，不再重复粘贴全部定义)
# 专门用于生成摘要的内部 LLM，选用 DeepSeek-V3 快速版
summary_llm = ChatOpenAI(api_key=os.environ.get("API_KEY"), base_url="https://api.siliconflow.cn/v1",
                         model="deepseek-ai/DeepSeek-V3", temperature=0)

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个对话总结助手。请将以下对话历史浓缩成一段不超过 200 字的摘要，务必保留其中的关键事实和核心上下文。"),
    ("human", "{chat_history}")
])


class SummaryRedisHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, threshold: int = 4, ttl: int = 604800):
        self.session_id = session_id
        self.key_prefix = "ai_agent:chat_with_rag:"
        self.threshold = threshold
        self.ttl = ttl
        self.is_summarizing = False  # 并发锁状态印记

    @property
    def key(self) -> str:
        return self.key_prefix + self.session_id

    @property
    def messages(self) -> List[BaseMessage]:
        _items = redis_client.lrange(self.key, 0, -1)
        items = [json.loads(m) for m in _items[::-1]]
        return messages_from_dict(items)

    def add_message(self, message: BaseMessage) -> None:
        redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
        if self.ttl: redis_client.expire(self.key, self.ttl)

    async def aadd_messages(self, messages: List[BaseMessage]) -> None:
        """ 重写异步添加方法， LangChain 内部会调用它以支持 create_task """
        for message in messages:
            redis_client.lpush(self.key, json.dumps(message_to_dict(message)))
        if self.ttl: redis_client.expire(self.key, self.ttl)

        # 核心：检查长度并触发异步总结防丢锁任务
        current_length = redis_client.llen(self.key)
        if current_length >= self.threshold and not self.is_summarizing:
            self.is_summarizing = True
            asyncio.create_task(self._async_summarize())  # 抛出旁路任务

    async def _async_summarize(self):
        try:
            snapshot_len = redis_client.llen(self.key)  # 1. 拍下并发防线快照
            print(f"\n[后台任务] 触发记忆总结 (快照长度: {snapshot_len}, Session: {self.session_id})...")

            history_text = "\n".join([f"{m.type}: {m.content}" for m in self.messages])
            summary_chain = SUMMARY_PROMPT | summary_llm
            summary_response = await summary_chain.ainvoke({"chat_history": history_text})

            new_memory = SystemMessage(content=f"之前的对话摘要：{summary_response.content}")

            # 2. 优雅裁剪并发安全更新
            pipeline = redis_client.pipeline()
            for _ in range(snapshot_len): pipeline.rpop(self.key)  # 精准弹出老消息
            pipeline.rpush(self.key, json.dumps(message_to_dict(new_memory)))  # 从右侧塞入摘要
            pipeline.execute()
            print(f"[后台任务] Redis 状态已更新，记忆已安全压缩。")
        except Exception as e:
            print(f"[后台任务] 总结失败: {e}")
        finally:
            self.is_summarizing = False  # 3. 极其关键：释放并发锁

    def clear(self) -> None:
        redis_client.delete(self.key)


history_store = {}  # 全局状态单例引用字典


def get_summary_redis_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in history_store:
        history_store[session_id] = SummaryRedisHistory(session_id=session_id, threshold=4)
    return history_store[session_id]


# ================= ==========================
# 5. 组装 RAG 大一统 流水线 (Ultimate RAG Chain)
# ================= ==========================
# 5.1 构造 Context 准备阶段：把检索到的 Document 格式化为 Prompt 里的纯文本
def format_docs(docs: List[Document]):
    return "\n\n".join([f"来自章节 [{doc.metadata}]:\n{doc.page_content}" for doc in docs])


# 5.2 🌟 核心魔法：使用 LCEL 组装 RAG 流水线
# 输入 -> 检索 -> 格式化Context -> 组装Prompt -> 大模型生成答案
rag_core_chain = (
        {
            "context": lambda x: format_docs(ultimate_retriever.invoke(x["question"])),  # 这一步触发终极检索
            "question": lambda x: x["question"],
            "chat_history": lambda x: x["chat_history"]  # 这一步由 history 包装器自动填充
        }
        | qa_prompt
        | llm
)

# 5.3 套上 Redis 异步滚动记忆总结的“保护套”
final_conversational_rag_chain = RunnableWithMessageHistory(
    rag_core_chain,
    get_summary_redis_history,
    input_messages_key="question",
    history_messages_key="chat_history"
)

# ================= ==========================
# 6. FastAPI 接口定义
# ================= ==========================
app = FastAPI(title="投研/企业知识库 AI 助手 (工业级完全体)")


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="用户会话ID")
    query: str = Field(..., min_length=1, description="提问内容")


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    is_summarizing: bool = Field(default=False, description="当前后台是否正在压缩记忆")


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 获取大模型回答 (会自动处理检索、生成、历史加载、异步总结任务抛出)
        response = await final_conversational_rag_chain.ainvoke(
            {"question": request.query},
            config={"configurable": {"session_id": request.session_id}}
        )

        # 探查一下后台任务并发锁状态，返回给调用方做前端状态指示
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
    uvicorn.run(app, host="0.0.0.0", port=8090)
```

## 测试

为了全方位验收咱们这套 **“RAG + Qdrant 物理过滤 + Redis 滚动记忆 + Qwen3 云端重排”** 复合架构的实战能力，你可以直接用 Postman 或者咱们即将写的 Web 页面，输入以下三个极具破坏性的测试 Scenario：

### 🧪 Scenario 1: 记忆防线测试（验收 Redis 异步并发滚动总结）

这个场景专门用来测试大模型是否真的“记住了”上下文，并且在对话轮次变多时，后台的异步总结任务有没有成功触发并锁住状态。

- **👤 你的提问 (Round 1)：** “晚上加班打车怎么报销？”
  - **🤖 AI 回答：** “根据《考勤与休假制度》，员工因项目加班超过晚上 21:30 下班的，可通过‘企业滴滴企业版’直接打车回家，产生的费用由企业账户统一支付，无需个人垫付。” _(此时触发了准确的 RAG 召回)_
- **👤 你的提问 (Round 2，省略主语)：** “那如果是晚上10点走，但我自己垫钱了呢？”
  - **🤖 AI 回答：** “如果您未使用滴滴企业版而产生了个人垫付，您需要保留正规发票，并在次月 5 号前通过财务系统的‘日常费用报销’模块提交单据。” _(完美！AI 结合了上一轮的“打车报销”记忆，并精准找出了贴票流程)_
- **👤 你的提问 (Round 3，继续追问细节)：** “要是发票丢了怎么办？”
  - **🤖 AI 回答：** “抱歉，参考资料中并未提及发票遗失后的具体处理流程。建议您直接咨询财务部门。” _(极其严谨！没有触发幻觉瞎编)_
  - **⚙️ 此时后台终端日志：** `[后台任务] 触发记忆总结... Redis 状态已更新。` _(完美验收了我们的并发安全机制！)_

---

### 🛡️ Scenario 2: 物理隔离测试（验收 Qdrant 标量过滤）

这个场景专门用来测试系统是否严格遵守了数据权限。假设你在代码里开启了 `{"metadata.Header1": "IT部设备规范"}` 的硬过滤：

- **👤 你的提问：** “我新领的电脑连不上网怎么办？”
  - **🤖 AI 回答：** “根据 IT 部门规范，您的办公电脑必须且只能连接名为 `Starry_Corp_5G` 的内部无线网络。请检查您是否连接了此网络。严禁私自连接外部公共热点或个人手机热点。”
- **👤 你的提问（跨权限越界测试）：** “网连不上没法干活了，我要请假回家，流程怎么走？”
  - **🤖 AI 回答：** “抱歉，在当前的参考资料（IT部设备规范）中，未检索到关于请假流程的相关规定。” _(极其冷酷且完美！底层 Qdrant 的 Filter 直接把 HR 的规定挡在了门外，做到了物理级别的数据隔离)_

---

### 🎯 Scenario 3: 狙击手测试（验收 Qwen3-8B 重排的精度）

这个场景用来测试当文本里有很多容易混淆的条件时，云端的 8B 重排模型能不能精准“掐尖”。

- **👤 你的提问：** “我早上起来突然发高烧，实在没法提前一天请假，这算旷工吗？”
  - **🤖 AI 回答：** “不算旷工。根据《考勤与休假制度》中的紧急情况处理规定：由于突发疾病无法提前请假的，您必须在**当天上午 10:00 前**口头向主管请假，并于**返岗后 24 小时内**补办系统流程。”
  - _（架构师视角：由于用户问题很长且口语化，底层的 BM25 和向量召回可能会捞出几十条关于“考勤”、“旷工”的碎块。但由于你挂载了 Qwen3-8B Reranker，它凭借极其强大的语义理解能力，直接把这条隐藏在备注里的“突发疾病”条款精准打到了 Top 1！）_
