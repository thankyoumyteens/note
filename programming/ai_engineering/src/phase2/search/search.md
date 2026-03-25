# 高级检索技术与重排

在前面的阶段，我们用了“向量检索 + 标量过滤 (WHERE)”。但这依然存在两个致命的盲区：

1. 向量检索是个“文科生”，对具体数字和专有名词极度迟钝。
   - 假设用户搜：“Error-404 怎么解决？”或者“MacBook Pro M3 Max 怎么连网？”
   - 向量模型能看懂“报错”和“电脑连网”的语义，但它分不清 404 和 502 的区别，也分不清 M3 和 M2。它大概率会给你推一堆其他型号的连网教程。
2. 向量检索（Bi-encoder）打分太粗糙。
   - 为了保证能在几毫秒内搜完上百万条数据，向量模型是“提前”把文档算成向量存好的。检索时，只是简单地算一下问题向量和文档向量的“余弦夹角”。这就好比HR 看简历（初筛），只扫一眼关键字和大概背景，速度极快，但经常看走眼。

终极解决方案：三步走战略

1. 第一步： Sparse Retrieval (稀疏检索 / 传统关键词检索)。比如大名鼎鼎的 BM25 算法（Elasticsearch 的核心）。它不懂语义，但它是“找茬大师”，只要字面上有 Error-404，它就能精准揪出来。
2. 第二步： Ensemble (融合双路召回)。把“向量（懂意思）”和“BM25（抠字眼）”搜出来的结果按权重合并，比如一共捞出 20 条候选数据。
3. 第三步： Reranker (重排模型 / Cross-encoder)。这相当于部门主管亲自面试（精排）。重排模型不提前存数据，它是在拿到那 20 条候选数据后，把“用户的问题”和“每一条文档”放在一起，逐字逐句地交叉阅读，给出一个极其精准的匹配分，最后只挑出最完美的 Top 3 喂给大模型。

## LangChain 终极检索流水线

### 1. 安装依赖

```sh
pip install rank_bm25 langchain-huggingface sentence-transformers langchain-qdrant langchain-openai langchain-ollama
pip install --upgrade setuptools
```

### 2. 代码

```py
import os

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

from silicon_flow_components import SiliconFlowReranker

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.retrievers import BM25Retriever
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever

SILICON_FLOW_API_KEY = os.environ.get("OPENAI_API_KEY")

# ==========================================
# 0. 准备极端测试数据
# ==========================================
docs = [
    Document(page_content="关于 MacBook Pro M2 芯片的连网指南：请打开右上角 Wi-Fi。"),
    Document(page_content="关于 MacBook Pro M3 Max 芯片的连网指南：请使用企业级 5G 认证。"),
    Document(page_content="公司食堂明天的菜谱是红烧肉。"),
    Document(page_content="Windows 电脑的连网报错 Error-404 解决办法。")
]

query = "MacBook Pro M3 Max 怎么连网？"
print(f"🔍 用户提问: {query}\n")

# ==========================================
# 1. 第一路召回：BM25 关键词检索 (Sparse)
# ==========================================
print("1. 正在初始化 BM25 关键词检索器...")
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 2

# ==========================================
# 2. 第二路召回：Qdrant 向量检索 (Dense)
# ==========================================
print("2. 正在加载 Embedding 模型...")
embeddings = OpenAIEmbeddings(
    openai_api_key=SILICON_FLOW_API_KEY,  # 你的硅基流动 API Key
    openai_api_base="https://api.siliconflow.cn/v1",  # 替换为硅基流动的网关
    model="Qwen/Qwen3-Embedding-8B"
)
vectorstore = QdrantVectorStore.from_documents(
    docs,
    embeddings,
    url="http://localhost:6333",
    collection_name="advanced_hybrid_test",
    force_recreate=True  # 让 Qdrant 自动重建表
)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ==========================================
# 3. 融合检索 (Ensemble) —— HR 初筛完毕
# ==========================================
print("3. 正在组装双路融合检索器 (Ensemble)...")
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)

print("\n--- 🟡 仅通过双路召回 (未重排) 的结果 ---")
ensemble_docs = ensemble_retriever.invoke(query)
for i, doc in enumerate(ensemble_docs):
    print(f"候选 {i + 1}: {doc.page_content}")

# ==========================================
# 4. 终极杀器：引入 BGE-Reranker (主管精排)
# ==========================================
print("\n⚙️ 正在调用硅基流动云端 API 进行深度重排...")
compressor = SiliconFlowReranker(api_key=SILICON_FLOW_API_KEY, top_n=1)

final_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=ensemble_retriever
)

# ==========================================
# 5. 见证奇迹的时刻
# ==========================================
print("\n--- 🟢 经过 Reranker 重排后的最终结果 ---")
final_docs = final_retriever.invoke(query)
for i, doc in enumerate(final_docs):
    print(f"🏆 Top {i + 1} [绝对精准匹配]: {doc.page_content}")

# ==========================================
# 6. 核心生成篇：构建 Prompt 与 LLM 对接
# ==========================================
print("\n" + "=" * 50)
print("🚀 阶段三：将检索结果喂给大模型 (Generate)")
print("=" * 50)

# 1. 实例化大模型
llm = ChatOpenAI(
    api_key=SILICON_FLOW_API_KEY,
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    temperature=0.1  # RAG 场景下，温度设低一点，让它严谨客观，不要发散
)

# 2. 撰写极其严苛的系统提示词模板 (Prompt Template)
system_prompt = (
    "你是一个极其严谨的企业内部 IT 助手。"
    "你的唯一任务是使用下面提供的【参考资料】来回答用户的提问。"
    "核心纪律："
    "1. 如果【参考资料】中没有包含答案，你必须直接回答‘抱歉，知识库中未找到相关规定’，绝不允许根据你的常识进行捏造！"
    "2. 回答要言简意赅，态度专业。\n\n"
    "【参考资料】：\n"
    "{context}"
)

# 组合成 LangChain 标准的聊天模板
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# 3. 组装组装文档链 (把检索出的文档塞进 prompt 的 {context} 变量里)
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# 4. 组装终极 RAG 检索链条
# 这里的 final_retriever 就是我们之前千辛万苦做的“BM25 + 向量 + 重排”的终极检索器
rag_chain = create_retrieval_chain(final_retriever, question_answer_chain)

# ==========================================
# 7. 见证完全体 RAG 系统的诞生
# ==========================================
print("🧠 大模型正在阅读检索资料并思考答案...\n")

# 触发整个链条：接收问题 -> 触发检索器 -> 拿到资料 -> 填入 Prompt -> 调用大模型 -> 返回结果
response = rag_chain.invoke({"input": query})

print("🤖 最终 AI 回答：")
print(response["answer"])
```

当这段代码跑起来，你会看到：

1. 在未重排阶段，系统可能会把 M2 和 M3 的数据都丢给你，因为它们在字面上和语义上都太像了。
2. 但经过 Reranker 交叉审阅后，系统犹如开了“火眼金睛”，无情地砍掉了 M2 的干扰项，只把那条唯一的 M3 Max 精确结果端到了你面前！
