# Qdrant 向量数据库

Qdrant 是用 Rust 编写的，极其轻量、性能极高，而且单机跑 Docker 非常稳，API 设计也极其优雅。

## 启动 Qdrant

```sh
# 拉取并运行 Qdrant 镜像，暴露 6333 (HTTP API) 和 6334 (gRPC) 端口
docker run -p 6333:6333 -p 6334:6334 \
    -v ~/tmp/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

`-v` 参数将数据挂载到了你物理机的 qdrant_storage 文件夹下，实现了真正的持久化。哪怕重启容器，数据也不会丢。

运行成功后，你甚至可以在浏览器里访问 [http://localhost:6333/dashboard](http://localhost:6333/dashboard)，Qdrant 自带了一个非常漂亮的 Web UI 管理控制台！

## 向量数据库的 CRUD

在接入 LangChain 之前，作为后端，我们必须先用原生的 SDK 摸清数据库底层的增删改查逻辑。

### 1. 安装 Qdrant 的 Python 客户端

```sh
pip install qdrant-client langchain-huggingface
```

### 2. 代码

```py
import os

# 使用 Hugging Face 国内镜像源
# os.environ 的配置，必须放在你 import HuggingFace 相关库的前面！
# 一旦先 import 了底层库，它就会读取系统默认的环境变量，你再改就晚了。
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_huggingface import HuggingFaceEmbeddings
import uuid

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

# 1. 连接数据库
print("🔌 正在连接 Qdrant 数据库...")
client = QdrantClient(url="http://localhost:6333")

# 我们先定义我们要用的 Embedding 模型（这里继续用免费高效的本地 BGE 模型）
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5", model_kwargs={'device': 'cpu'})

# BGE-small 输出的向量长度固定是 512 维（如果是 OpenAI 的 text-embedding-3-small 则是 1536 维）
VECTOR_DIMENSION = 512

# 2. 建表 (Create Collection)
# 相当于 SQL: CREATE TABLE company_rules (...)
COLLECTION_NAME = "company_rules"
if not client.collection_exists(COLLECTION_NAME):
    print(f"📦 创建集合: {COLLECTION_NAME}")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_DIMENSION,
            distance=Distance.COSINE  # 使用余弦相似度计算距离
        ),
    )

# 3. 准备数据 (假设这是我们切分好的 Chunk)
docs = [
    {"text": "公司每月随工资发放800元餐饮补贴。", "category": "福利", "department": "HR"},
    {"text": "办公电脑需连接Starry_Corp_5G网络。", "category": "IT", "department": "IT部"},
    {"text": "加班超过晚上21:30可报销打车费。", "category": "福利", "department": "HR"}
]

# 把文本变成向量
print("🧠 正在调用模型将文本转为向量...")
texts = [doc["text"] for doc in docs]
vectors = embeddings.embed_documents(texts)

# 4. 批量写入 (Batch Insert)
print("💾 正在批量写入数据库...")
points = []
for i, vector in enumerate(vectors):
    point = PointStruct(
        id=str(uuid.uuid4()),  # 主键 ID (必须是 UUID 或正整数)
        vector=vector,  # 核心：高维向量数组
        payload=docs[i]  # 附加的 Metadata（原文和标签），在 Qdrant 里叫 Payload
    )
    points.append(point)

# 执行插入
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)
print("✅ 写入完成！")

# 5. 相似度查询 (Similarity Search) - RAG 的核心！
query = "我加班晚了怎么回家？"
print(f"\n🔍 用户提问: {query}")
# 先用模型把问题变成向量
query_vector = embeddings.embed_query(query)

# 相当于 SQL: SELECT * FROM company_rules ORDER BY vector_distance LIMIT 2
search_result = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=2  # 找最相似的前两名 (Top-K)
)

print("\n🎯 检索结果：")
for hit in search_result.points:
    # score 是余弦相似度得分，越接近 1 越相似
    print(f"-> [相似度: {hit.score:.4f}] 文本: {hit.payload['text']} (分类: {hit.payload['category']})")
```
