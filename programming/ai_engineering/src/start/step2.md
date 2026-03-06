# 打通真实的文档数据流（ETL 与分块）

在真实的业务场景中，知识库不可能手动写死在代码里。我们需要让程序自动读取外部文件，清洗数据，并存入向量数据库。

### 1. 准备一份真实的“业务文档”

在项目根目录下创建一个名为 research_report.md 的文本文件，模拟一份包含深度财务分析的研报

```markdown
# 2026年科技与价值投资策略研报

## 一、 Palantir (PLTR) 核心业务与估值分析

Palantir 作为企业级 AI 应用的领军者，其核心增长引擎 AIP（人工智能平台）在商业领域的渗透率持续提升。区别于传统 SaaS 公司，Palantir 擅长处理极其复杂的异构数据本体（Ontology）。在估值层面，由于其尚未派发股息（Dividend），传统的股息贴现模型（DDM）并不适用，市场更多采用市销率（P/S）和自由现金流收益率来进行相对估值。

## 二、 价值投资与高股息策略

在宏观经济波动期，采用经典的价值投资原则构建防御性投资组合显得尤为重要。投资者应重点关注具有宽广护城河、稳定盈利能力以及持续派息记录的企业。
核心筛选指标包括：

1. 股息率（Dividend Yield）持续稳定在 4% 以上。
2. 盈利收益率（Earnings Yield，即市盈率的倒数）显著高于无风险利率。
3. 派息比率（Payout Ratio）健康，通常低于 70%，确保企业有足够的留存收益用于未来发展。
```

### 2. 编写“离线数据灌库”脚本 (ETL)

这个脚本相当于你以前写的批处理 Job（如 XXL-JOB）。它的任务是：读取文件 -> 切割文本 -> 转为向量 -> 持久化到磁盘。

在项目下新建一个文件 ingest.py

```py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_vector_db():
    print("1. 正在加载本地文档...")
    # 使用 TextLoader 加载 Markdown 文件
    loader = TextLoader("research_report.md", encoding="utf-8")
    documents = loader.load()

    print("2. 正在进行文本切块 (Chunking)...")

    # 初始化文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # 每个分块最大包含 200 个字符
        chunk_overlap=50,  # 相邻分块重叠 50 个字符（防止一句话被从中间硬生生切断）
        separators=["\n\n", "\n", "。", "！", "？", "，", " "]  # 优先按段落切，其次按句子切
    )
    # 将一长篇文档切成一个个小的 Document 对象
    chunks = text_splitter.split_documents(documents)
    print(f"文档切分完毕，共切分为 {len(chunks)} 个数据块。")

    print("3. 正在初始化 BGE 向量模型...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    print("4. 正在计算向量并构建 FAISS 本地索引...")
    # 将分块后的文本喂给模型，计算向量，并存入 FAISS
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 5. 持久化到本地磁盘 (相当于把内存数据落盘)
    vectorstore.save_local("faiss_index_db")
    print("🎉 知识库构建完成！已保存到当前目录的 faiss_index_db 文件夹中。")


if __name__ == "__main__":
    build_vector_db()
```

在终端执行 python ingest.py。你会看到项目目录下多了一个 faiss_index_db 文件夹，里面有 .faiss 和 .pkl 文件。这就相当于你本地的 MySQL 数据文件！

### 3. 改造 FastAPI 接口

现在，main.py 不再需要每次启动时都去重新计算那堆写死的文字了。它只需要去读取刚才生成的本地数据库。

```py
# ... 前面直到定义响应体 DTO 的部分都保持不变 ...

# 3. 初始化 RAG 知识库 (模拟企业私有数据注入)

print("正在启动服务，加载本地向量数据库...")

# 只需要初始化本地词嵌入模型 (必须和存数据时用的一样)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

# 从本地磁盘加载 FAISS 索引 (读写分离！)
# allow_dangerous_deserialization=True 是必须的，表示你信任本地的 pickle 文件
vectorstore = FAISS.load_local(
    "faiss_index_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# 这里稍微做个优化：把检索数量从 k=1 改成 k=2，给大模型更多上下文
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ... 后面的 llm 初始化、prompt 模板、rag_chain 和 @app.post 接口完全保持不变 ...
```

### 4. 重启你的 FastAPI 服务

然后在 Swagger UI 中，尝试提问这两个问题：

1. 评估 Palantir 时，为什么传统的股息贴现模型不适用？建议用什么指标？
2. 构建高股息策略时，对于派息比率有什么要求？

看看它是否能从刚才生成的离线数据库中准确捞出数据并回答。
