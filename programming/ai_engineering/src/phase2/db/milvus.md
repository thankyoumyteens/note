# Milvus 向量数据库

如果说 Qdrant 是轻巧锐利的“瑞士军刀”，那么由 Zilliz 团队主导开源的 Milvus 就是向量数据库界的“Hadoop / 繁星架构”——它是为十亿、百亿级高并发企业级检索而生的。

## 安装 Milvus

```sh
# 1. 下载官方的单机版 docker-compose 编排文件
curl -O https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/docker/standalone/docker-compose.yml

# 2. 一键启动包含 Milvus、etcd 和 MinIO 的微服务集群
docker-compose up -d

# 3. 查看是否启动成功（应该能看到 3 个状态为 Up 的容器）
docker-compose ps
```

## 向量数据库的 CRUD

### 1. 安装 Milvus 依赖包

```sh
pip install pymilvus sentence-transformers
```

### 2. 用 Milvus 重写 CRUD

你会发现，虽然底层引擎换了，但作为架构师，我们抽象出来的业务逻辑（定义表 -> 向量化 -> 写入 -> 检索）是完全一致的。

```py
import os

import env_setup

import time
from pymilvus import MilvusClient
from langchain_openai import OpenAIEmbeddings

# 1. 初始化 Milvus Lite 客户端
print("🔌 正在连接 Docker 版 Milvus 服务器 (端口 19530)...")
client = MilvusClient(uri="http://localhost:19530")

COLLECTION_NAME = "company_rules"

# 2. 建表 (Create Collection)
# 传统后端秒懂：如果表存在就先删掉（为了方便我们反复测试）
if client.has_collection(collection_name=COLLECTION_NAME):
    client.drop_collection(collection_name=COLLECTION_NAME)

print(f"📦 创建 Milvus 集合: {COLLECTION_NAME}")
VECTOR_DIMENSION = 512
# Milvus 相比 Qdrant 更加严格，但新版的高级 API 帮我们简化了 Schema 的创建
client.create_collection(
    collection_name=COLLECTION_NAME,
    dimension=VECTOR_DIMENSION,  # 维度
    metric_type="COSINE",  # 余弦相似度
    id_type="int",  # 主键类型
    auto_id=True  # 类似 MySQL 的 AUTO_INCREMENT
)

# 3. 准备数据并向量化
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B",
    dimensions=VECTOR_DIMENSION
)

docs = [
    {"text": "公司每月随工资发放800元餐饮补贴。", "category": "福利"},
    {"text": "办公电脑需连接Starry_Corp_5G网络。", "category": "IT"},
    {"text": "加班超过晚上21:30可报销打车费。", "category": "福利"}
]

print("🧠 正在调用模型将文本转为向量...")
vectors = embeddings.embed_documents([doc["text"] for doc in docs])

# 4. 组装数据并批量写入
# Milvus 接受的是一个字典列表（List of Dicts），键名就是字段名
data = []
for i in range(len(docs)):
    data.append({
        "vector": vectors[i],  # 核心高维向量
        "text": docs[i]["text"],  # 标量字段（原文）
        "category": docs[i]["category"]  # 标量字段（分类 Metadata）
    })

print("💾 正在批量写入 Milvus 数据库...")
res = client.insert(collection_name=COLLECTION_NAME, data=data)
print(f"✅ 成功写入 {res['insert_count']} 条数据！")

# 🌟 让主线程等一等底层的数据落盘
print("⏳ 等待分布式系统数据落盘构建索引...")
time.sleep(2)

# 5. 向量检索 (Vector Search)
query = "我加班晚了怎么回家？"
print(f"\n🔍 用户提问: {query}")
query_vector = embeddings.embed_query(query)

search_res = client.search(
    collection_name=COLLECTION_NAME,
    data=[query_vector],  # 注意这里传入的是列表，支持一次性搜多个问题
    limit=2,  # Top-K
    output_fields=["text", "category"]  # 类似 SQL 里的 SELECT text, category
)

print("\n🎯 Milvus 检索结果：")
# 返回的结果是一个二维数组（因为支持批量检索），我们遍历第一层
for hits in search_res:
    for hit in hits:
        # distance 是距离/相似度，entity 里装着我们刚才 SELECT 出来的标量数据
        print(f"-> [相似度: {hit['distance']:.4f}] 文本: {hit['entity']['text']} (分类: {hit['entity']['category']})")
```

## Milvus vs Qdrant

- Qdrant 偏向于 NoSQL（像 MongoDB）。你的 Metadata 全部塞进一个叫 payload 的大 JSON 字段里，不用提前声明。
- Milvus 偏向于关系型数据库（像 MySQL）。在更底层的 API 中，你需要严格定义每一个 Field（比如 text 是 VARCHAR，vector 是 FLOAT_VECTOR），这在海量数据下性能更好、内存占用更低。
