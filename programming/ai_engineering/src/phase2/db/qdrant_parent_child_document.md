# 使用 Qdrant 的父子文档拆分

要用 Qdrant 完全替换掉 ParentDocumentRetriever 架构中的 Chroma，只需要引入最新的专属官方包 langchain_qdrant，并实例化一个空的 QdrantVectorStore 即可。

### 1. 安装依赖

```sh
pip install langchain-qdrant
```

### 2. 代码

```py
import json
import os

import env_setup

import redis
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.storage import RedisStore
from langchain_core.documents import Document
from langchain_classic.storage import EncoderBackedStore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

print("1. 正在读取并进行 Markdown 语义切分...")
with open("parsed_result.md", "r", encoding="utf-8") as f:
    markdown_document = f.read()

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

parent_docs = markdown_splitter.split_text(markdown_document)

print(f"切分出了 {len(parent_docs)} 个语义父块。示例 Metadata: {parent_docs[0].metadata}")

# 输出的向量维度
VECTOR_DIMENSION = 4096

print("加载 Embedding 模型...")
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B",
    # 指定输出的向量维度
    dimensions=VECTOR_DIMENSION
)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

# ========== 替换原有的 Chroma 代码 ===========
# 1. 初始化底层的 Qdrant 客户端
qdrant_client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "split_parents_qdrant"

# 2. 建表
if not qdrant_client.collection_exists(COLLECTION_NAME):
    print(f"📦 创建新表: {COLLECTION_NAME} (维度: {VECTOR_DIMENSION})")
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_DIMENSION,
            distance=Distance.COSINE
        ),
    )

# 3. 实例化空的向量库容器
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

print("连接 Redis 数据库...")
redis_client = redis.Redis.from_url("redis://localhost:6379/0")
redis_byte_store = RedisStore(client=redis_client, namespace="rag:parent_docs:")


def encode_doc(doc: Document) -> bytes:
    return json.dumps({
        "page_content": doc.page_content,
        "metadata": doc.metadata
    }).encode("utf-8")


def decode_doc(b: bytes) -> Document:
    data = json.loads(b.decode("utf-8"))
    return Document(page_content=data["page_content"], metadata=data.get("metadata", {}))


store = EncoderBackedStore(
    store=redis_byte_store,
    key_encoder=lambda x: x,
    value_serializer=encode_doc,
    value_deserializer=decode_doc
)

print("正在构建父子索引并写入 Redis / Qdrant...")
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=None,
)
retriever.add_documents(parent_docs)

query = "请假需要走什么流程？"

print("\n--- 1. 底层向量库直接匹配到的【子块】（极其零碎） ---")
sub_docs = vectorstore.similarity_search(query, k=1)
for doc in sub_docs:
    print(doc.page_content)

print("\n--- 2. ParentDocumentRetriever 最终返回的【父块】（上下文极其丰富） ---")
retrieved_docs = retriever.invoke(query)
for doc in retrieved_docs:
    print(doc.page_content)
```
