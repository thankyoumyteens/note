# 让AI记住上下文

在传统的 Java Web 开发中，HTTP 是无状态的，我们通过给用户发放 JSESSIONID 或 Token，在服务端的 Redis 里存储用户的 Session 状态。

在 AI 开发中，大模型同样是无状态的。它没有记忆，你每次调用 API，它都像一个失忆症患者。所谓“记忆”，就是我们在每次发送 HTTP 请求给大模型时，把之前的“聊天记录”强行拼接到提示词（Prompt）里一起发给它。

假如你的历史记录里有这样一段对话：

- 用户：请分析一下 Palantir 的核心业务。
- AI：Palantir 的核心是 AIP 平台...
- 用户：那它的估值方法是什么？

注意用户的第二个问题里的**“它”**。如果你直接把“那它的估值方法是什么？”丢给向量数据库（FAISS）去检索，根本查不到任何有用的文档，因为数据库不知道“它”是谁。

因此，带记忆的 RAG 必须分为两步：

1. 问题重写（Query Condense）：先让大模型结合历史记录，把“那它的估值方法是什么？”改写成独立、完整的“Palantir 的估值方法是什么？”。
2. 检索与回答（Retrieve & Generate）：拿着改写后的完整问题，去查向量库，然后再结合历史记录给出最终回答。

### 1. 改造 main.py

需要引入 LangChain 最新的历史记录管理工具。

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# === 新增的 Memory 与 Chain 相关依赖 ===
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ================= 豆包 (Volcengine) 配置区 =================
DOUBAO_API_KEY = "替换"
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
LLM_ENDPOINT_ID = "ep-11111111111111-aaaaa"
# =========================================================

app = FastAPI(title="My First RAG API")


# 改造 DTO：增加 session_id 字段以区分不同用户的会话
class QueryRequest(BaseModel):
    session_id: str  # 类似 JSESSIONID
    query: str


class QueryResponse(BaseModel):
    answer: str


print("正在启动服务，加载本地向量数据库...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
vectorstore = FAISS.load_local(
    "faiss_index_db",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

llm = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model=LLM_ENDPOINT_ID,
    temperature=0,
    max_tokens=1024
)

# 模拟 Redis 存储 Session (内存字典)
# 相当于 Java 里的 ConcurrentHashMap<String, ChatMessageHistory>
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # ChatMessageHistory 是存到内存中的
        # 如果引入了 Redis
        # 可以把 ChatMessageHistory 替换成 LangChain 官方提供的 RedisChatMessageHistory
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# 核心逻辑 A：历史感知检索器 (History-Aware Retriever)
# 作用：结合历史记录，把代词（它、这个）改写成明确的名词
contextualize_q_system_prompt = (
    "给定聊天历史记录和最新的用户问题，该问题可能会引用历史记录中的上下文。"
    "请根据历史记录，将最新的问题重写为一个独立、完整的问题（不要包含代词）。"
    "如果你认为问题不需要重写，请原样返回。"
    "注意：只需返回重写后的问题，绝对不要回答它！"
)
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),  # 这是一个占位符，LangChain 会自动把历史 Message 列表填入这里
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

# 核心逻辑 B：问答链 (QA Chain)
# 作用：拿着检索到的文档，结合历史记录，生成最终答案
qa_system_prompt = (
    "你是一个专业的分析师。请严格基于以下<context>中的信息来回答问题。\n"
    "如果你不知道答案，请直接说不知道。\n\n"
    "<context>\n{context}\n</context>"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 将检索器和问答链组合起来
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 5. 最终包装：自动注入与保存历史记录的拦截器 (Interceptor)
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,  # 获取历史记录的函数
    input_messages_key="input",  # 告诉框架，用户的输入对应哪个变量
    history_messages_key="chat_history",  # 告诉框架，历史记录应该放进哪个占位符
    output_messages_key="answer",  # 告诉框架，把大模型的哪个输出保存到历史记录里
)


@app.post("/api/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    try:
        # 调用时必须传入 config，指定 session_id
        result = conversational_rag_chain.invoke(
            {"input": request.query},
            config={"configurable": {"session_id": request.session_id}}
        )
        return QueryResponse(answer=result["answer"])
    except Exception as e:
        # 全局异常捕获
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. 进行测试体验

1. 请求 1：
   ```json
   {
     "session_id": "user-walter-123",
     "query": "研报中提到了哪家科技公司的估值分析？"
   }
   ```
2. AI 回答：提到了 Palantir (PLTR) ...
3. 请求 2（关键的上下文测试）：
   ```json
   {
     "session_id": "user-walter-123",
     "query": "为什么它的估值不能用传统的股息贴现模型？"
   }
   ```
   注意：你的问题里只有“它”，没有提 Palantir。此时，AI 的“问题重写”模块会发挥作用，成功查到并返回因为其尚未派发股息等原因。
4. 请求 3（换一个 Session 测试隔离性）：
   ```json
   {
     "session_id": "user-walter-456",
     "query": "我刚才问了关于哪家公司的问题？"
   }
   ```
   AI 应该回答不知道，因为这个新的 session_id 下没有任何记忆。
