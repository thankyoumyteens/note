# 标量过滤

在大模型的 RAG 世界里，检索分为两套截然不同的逻辑：

- 向量检索 (Vector Search)：它是基于“语义相似度”的模糊搜索。
  - 特点：懂意思，但没边界。
  - 痛点：比如你问“IT部怎么报销打车费？”，如果全公司只有“福利部”有打车规章，向量检索依然会把“福利部”的规章推给你，因为它觉得“报销打车费”这个语义极其匹配。这就导致了 AI 的串台和幻觉。
- 标量过滤 (Scalar Filtering)：就是传统的 SQL WHERE 条件。
  - 标量是什么：就是单个的具体数值（字符串、整数、布尔值）。也就是我们在清洗数据时提取的 Metadata（如 `department = 'IT部'`）。
  - 特点：极其冷酷的精确匹配。不符合条件的，直接在物理层面剔除。

将两者结合（混合检索的初级形态），用你熟悉的 SQL 映射过来就是：

```sql
SELECT * FROM 知识库 WHERE department = 'IT部' ORDER BY 向量相似度(问题, 文本) LIMIT 5
```

## 在 Qdrant 中增加标量过滤

```py
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from qdrant_client import QdrantClient, models
from langchain_huggingface import HuggingFaceEmbeddings
import uuid

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

print("🔌 连接本地 Docker 里的 Qdrant 数据库...")
client = QdrantClient(url="http://localhost:6333")

# 2. 建表
COLLECTION_NAME = "review_scalar_filter"
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=512,
            distance=models.Distance.COSINE  # 使用余弦相似度计算距离
        )
    )

# 3. 准备数据 (注意这里的 Metadata 标签！)
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5", model_kwargs={'device': 'cpu'})
docs = [
    {"text": "公司每月随工资发放800元餐饮补贴。", "department": "HR部"},
    {"text": "办公电脑需连接Starry_Corp_5G网络。", "department": "IT部"},
    # 注意这条：它是关于打车报销的，但属于 HR 部
    {"text": "加班超过晚上21:30可报销打车费。", "department": "HR部"}
]

print("🧠 向量化并写入数据...")
vectors = embeddings.embed_documents([doc["text"] for doc in docs])
client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=vectors[i],
            payload=docs[i]  # payload 就是存储标量 Metadata 的地方
        )
        for i in range(len(docs))
    ]
)

# ==========================================
# 4. 见证魔法：带过滤的混合检索
# ==========================================
# 用户的提问在语义上 100% 偏向“打车报销”
query = "我加班晚了怎么报销打车费？"
print(f"\n🔍 用户提问: {query}")
query_vector = embeddings.embed_query(query)

print("🚨 开启标量过滤：强制要求 department 必须是 'IT部'！")

search_result = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    # 🌟 这里就是“硬过滤”的核心代码！
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="department",  # 去 payload 里找 department 字段
                match=models.MatchValue(value="IT部")  # 值必须严格等于 "IT部"
            )
        ]
    ),
    limit=2
)

print("\n🎯 最终检索结果：")
for hit in search_result.points:
    print(f"-> [相似度: {hit.score:.4f}] 文本: {hit.payload['text']} (部门: {hit.payload['department']})")
```

如果你运行这段代码，你会看到非常反直觉但极其正确的一幕：尽管用户满嘴都在问“打车报销”，但出来的结果只有一条：办公电脑需连接Starry_Corp_5G网络。 (部门: IT部)。

那条高相似度的“HR部”打车规定去哪了？被 query_filter 在底层直接“物理消灭”了。

## 为什么这一步在企业级架构中极其关键？

设想一个多租户的 SaaS 平台（比如飞书文档的 AI 助手）：

张三和李四的公司都在你的向量数据库里。张三搜“公司密码是什么”，如果没有标量过滤（`WHERE tenant_id = '张三的公司'`），你的向量检索大概率会把李四公司的密码搜出来喂给大模型。这就是极其严重的数据越权和安全事故！

标量过滤（Scalar Filtering）构成了 RAG 系统的“权限边界”和“逻辑护城河”。
