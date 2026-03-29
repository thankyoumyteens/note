# 标量过滤 + 父子文档拆分

注意底层的数据结构差异：

- 原生 Qdrant：你把数据存在 payload 里，它的层级是扁平的，所以你可以直接过滤 `key="department"`。
- LangChain 封装：LangChain 为了统一规范，它在往 Qdrant 存数据时，会把所有的元数据强行塞进一个名叫 metadata 的 JSON 对象里。所以在底层，它的 payload 长这样：`{"page_content": "...", "metadata": {"department": "IT部"}}`。

核心结论：在 LangChain 中使用 Qdrant 过滤，字段名必须加上 `metadata.` 前缀！（例如：`key="metadata.department"`）

```py
import os

import env_setup

import json
import redis
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.storage import EncoderBackedStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.documents import Document

from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore

from langchain_community.storage import RedisStore

# ==========================================
# 1. 加载本地真实业务文档 & Markdown 语义切分
# ==========================================
print("1. 正在读取本地 parsed_result.md 并进行语义切分...")
with open("parsed_result.md", "r", encoding="utf-8") as f:
    markdown_document = f.read()

# 按照 Markdown 标题提取带有层级关系的大块“父文档”
headers_to_split_on = [
    ("#", "Header1"),
    ("##", "Header2"),
    ("###", "Header3")
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
parent_docs = markdown_splitter.split_text(markdown_document)
print(f"-> 成功切分出 {len(parent_docs)} 个自带层级 Metadata 的父文档块。")

# ==========================================
# 2. 初始化环境 (云端 Embedding, Redis, Qdrant)
# ==========================================
VECTOR_DIMENSION = 512

print("\n2. 初始化云端 Embedding (维度压缩至 512)...")
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B",
    dimensions=VECTOR_DIMENSION
)

print("3. 连接本地 Redis 与 Qdrant...")
# --- Redis 配置 ---
redis_client = redis.Redis.from_url("redis://localhost:6379/0")
redis_byte_store = RedisStore(client=redis_client, namespace="rag:pure_parents:")


def encode_doc(doc: Document) -> bytes:
    return json.dumps({"page_content": doc.page_content, "metadata": doc.metadata}).encode("utf-8")


def decode_doc(b: bytes) -> Document:
    data = json.loads(b.decode("utf-8"))
    return Document(page_content=data["page_content"], metadata=data.get("metadata", {}))


store = EncoderBackedStore(
    store=redis_byte_store, key_encoder=lambda x: x, value_serializer=encode_doc, value_deserializer=decode_doc
)

# --- Qdrant 配置 ---
qdrant_client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "pure_company_kb"

if not qdrant_client.collection_exists(COLLECTION_NAME):
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_DIMENSION, distance=models.Distance.COSINE)
    )

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

# ==========================================
# 4. 组装带“硬性标量过滤”的 ParentDocumentRetriever
# ==========================================
print("\n4. 正在构建父子文档检索器 (已开启底层标量过滤)...")
child_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)

# 🚨 标量过滤的核心
# 假设你想把检索范围“死死锁定”在某一个具体的章节下
# 注意：务必根据你 parsed_result.md 里真实的标题层级来修改这里的值！
strict_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="metadata.Header2",  # 👈 核心：LangChain 强制要求加 metadata. 前缀
            match=models.MatchValue(value="第二十九条 休假")  # 换成你文档里真实存在的一级或二级标题
        )
    ]
)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=None,
    # 🌟 在这里把原生 filter 再次透传给底层！
    search_kwargs={
        "k": 2,
        "filter": strict_filter
    }
)

# 启动灌库动作：自动将 parent_docs 切碎存入 Qdrant，大块原文存入 Redis
print("-> 正在将子块向量写入 Qdrant，父块文本存入 Redis (请稍候)...")
retriever.add_documents(parent_docs)

# ================= 见证纯净版检索结果 =================
print("\n" + "=" * 50)
query = "请假需要走什么流程？"  # 建议换成你 parsed_result.md 里实际涵盖的内容

print(f"🔍 用户提问: {query}")
print("🧠 触发纯净版 [Qdrant 向量匹配 -> Redis 原文回表] 流水线...")

retrieved_docs = retriever.invoke(query)

print("\n🏆 【检索结果】:")
if not retrieved_docs:
    print("-> 🈳 未检索到相关内容。")
else:
    for i, doc in enumerate(retrieved_docs):
        print(f"\n--- 结果 {i + 1} ---")
        print(f"【所属章节】: {doc.metadata}")
        print(f"【完整内容】: {doc.page_content}")
print("=" * 50)
```
