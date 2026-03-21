# 父子文档拆分

作为一个有后端经验的开发者，你可以把今天我们要学的父子文档拆分（Parent-Child Document）完美映射为数据库中的“二级索引与回表查询”：

1. 我们用非常细粒度的字段（子块/Child Chunk）去建立高精度的向量索引。
2. 一旦命中这个细粒度索引，我们不直接把局部数据丢给前端，而是拿到主键 ID，去主表里 **“回表”**，把包含这条数据的完整大记录（父块/Parent Chunk）取出来，喂给大模型。

假设你的文档里有这样一段话：

```
“星辰科技的餐补制度：公司每月随工资发放 800 元餐饮补贴。此外，如果是周末加班，额外提供 50 元/天的补助。”
```

- 如果切块太大（比如 1000 字一段）：用户搜“周末加班补助多少钱”，因为这 1000 字里讲了考勤、绩效、年假等各种东西，“周末补助”的语义被稀释了，向量匹配的得分会很低，导致检索失败。
- 如果切块太小（比如按句话切，50 字一段）：检索非常精准，系统完美命中了“此外，如果是周末加班，额外提供 50 元/天的补助。”这句话。但是！你把这句话单拎出来喂给 LLM，LLM 根本不知道这是哪个公司的、什么前提下的补助，它没有上下文。

父子文档机制完美解决了这个悖论：它在底层把这段话切成一句一句存入向量库（保证检索高命中率），但在给大模型时，它会把这一整段（甚至整章）一起拿出来（保证上下文完整）。

## 实现 Parent-Child Document Retriever

在 LangChain 中，实现这个功能需要配合一个额外的组件：文档存储（Document Store）。

- 向量数据库（Chroma）：用来存子块的向量，负责“搜索”。
- 文档存储（InMemoryStore/Redis 等）：用来存父块的原文，负责“回表”。

### 1. 安装依赖

```sh
pip install langchain langchain-chroma langchain-huggingface
```

### 2. 代码

```py
import os

from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.documents import Document
from langchain_core.stores import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 配置环境变量以加速模型下载
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 1. 准备一份测试文档（模拟一个比较长、结构化的段落）
docs = [
    Document(
        page_content="""
        【第三章：假期与福利】
        1. 年假：试用期（3个月）通过后，即可获得每年 12 天的带薪年假。工作满3年后，年假增加至 15 天。
        2. 病假：每人每月享有 1 天带薪病假。连续请病假超过 2 天的，需要提供三甲医院开具的病假证明。
        3. 餐补：公司每月随工资发放 800 元餐饮补贴。若因项目加班超过晚上 21:30，可通过企业滴滴企业版直接打车回家，费用由公司全额企业支付。
        """,
        metadata={"source": "员工手册2026.pdf"}
    )
]
# 实际可以使用这个读取文档: docs = TextLoader("员工手册2026.md", encoding="utf-8").load()

# 2. 初始化本地 Embedding 模型
print("加载 Embedding 模型...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

# 3. 初始化两种切分器：一个切大块（父），一个切小块（子）
# 父文档切分器：尽量保持一个大段落的完整性（比如 400 字一块）
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)

# 子文档切分器：切得很细，尽量是一两句话（比如 50 字一块），用于精准匹配
child_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)

# 4. 初始化底层的存储
# 向量数据库：存小块 (Child)
vectorstore = Chroma(collection_name="split_parents", embedding_function=embeddings)
# 内存文档存储：存大块 (Parent) -> 实际生产中这里经常换成 Redis 或 MongoDB
store = InMemoryStore()

# 5. 核心魔法：组装 ParentDocumentRetriever
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# 6. 将文档加入检索器（这一步系统会自动切分父子块，并建立关联映射）
print("正在构建父子文档索引...")
retriever.add_documents(docs)

# ================= 见证奇迹的时刻 =================

# 测试问题：极其细节的提问
query = "加班到几点可以报销打车费？"

# 传统的底层向量检索（看看子块匹配到了什么）
print("\n--- 1. 底层向量库直接匹配到的【子块】（极其零碎） ---")
sub_docs = vectorstore.similarity_search(query, k=1)
for doc in sub_docs:
    print(doc.page_content)
    # 你会看到类似："若因项目加班超过晚上 21:30，可通过企业滴滴企业版直接打车回家"
    # 注意：如果把这句话直接给 LLM，它可能不知道这是哪个部门、哪章的规定。

# 经过父文档检索器封装后的结果（回表后的数据）
print("\n--- 2. ParentDocumentRetriever 最终返回的【父块】（上下文极其丰富） ---")
retrieved_docs = retriever.invoke(query)
for doc in retrieved_docs:
    print(doc.page_content)
    # 你会看到包含了整段【第三章：假期与福利】的完整大段落！
```
