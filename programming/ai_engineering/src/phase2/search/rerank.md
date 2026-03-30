# LangChain 终极检索流水线

### 1. 安装依赖

```sh
pip install rank_bm25 sentence-transformers langchain-qdrant langchain-openai
pip install --upgrade setuptools
```

### 2. 数据准备

请在你的项目根目录下新建一个名为 parsed_result.md 的文件，并将以下全部内容直接复制进去保存：

```
# 考勤与休假制度

## 工作时间与日常考勤
员工的工作时间为标准工时制，各部门另有规定的从其规定。
标准工作时间为周一至周五，上午 9:30 至下午 18:00，其中 12:00 至 13:00 为午休时间。
员工上下班必须进行企业微信或钉钉打卡，每月允许有两次、每次不超过 30 分钟的迟到豁免机会。

## 请假与审批流程
为了规范员工休假管理，保障公司各项业务的正常运转，特制定本请假流程。
员工请假需要走以下标准化流程：
1. 员工需提前至少 1 个工作日在系统内的“考勤打卡”模块中提交请假申请单。
2. 请假天数在 1 天（含）以内的，由直属部门主管审批即可生效。
3. 请假天数在 1 天以上、3 天（含）以内的，需经直属部门主管审批后，流转至部门总监进行复批。
4. 请假天数超过 3 天的，除总监审批外，还须经 HRBP 及分管副总裁最终签批。
注意：突发疾病等紧急情况无法提前请假的，必须在当天上午 10:00 前口头向主管请假，并于返岗后 24 小时内补办系统流程。

## 加班与打车报销福利
关于晚间加班的交通报销标准及相关福利制度如下：
员工因项目紧急情况加班，超过晚上 21:30 下班的，可通过“企业滴滴企业版”直接打车回家。产生的打车费由企业账户统一支付，员工无需个人垫付和贴票报销。
若因特殊原因未使用滴滴企业版，员工需保留正规发票，并在次月 5 号前通过财务系统的“日常费用报销”模块提交单据。


# IT部设备规范

## 办公设备借用与归还
新入职员工在入职当天可凭 IT 领用工单前往 IT 运维部领取标准配置的笔记本电脑及外设。
员工离职时，必须在最后工作日将所有 IT 设备归还，并由 IT 运维部出具设备完好证明，方可办理结薪手续。

## 内部网络与信息安全
所有新入职员工的办公电脑，必须且只能连接名为 Starry_Corp_5G 的内部无线网络。
严禁员工私自将办公电脑连接外部公共热点或个人手机热点，以防范公司机密代码或商业数据发生泄露。违反此规定造成重大数据安全事故者，公司将保留追究法律责任的权利。
```

### 3. 云端重排组件

LangChain 作为一个全球化的通用大厦底座，它原生内置了对国际巨头（比如 OpenAI、Cohere 的 CohereRerank）的开箱即用支持。

但是，对于像硅基流动（SiliconFlow）这样的云服务商，LangChain 官方社区的更新是有滞后性的。官方包里压根就没有预置针对它的现成类。如果不自己写，我们就没法把硅基流动提供的重排模型塞进 LangChain 的流水线里。

LangChain 的流水线设计极其严谨，它规定了：任何想作为“重排器”接入流水线的组件，必须继承 BaseDocumentCompressor 这个父类，并且实现 compress_documents 方法。

只要我们守规矩继承了这个类，LangChain 就会把我们的自定义 HTTP 请求完美当成一个本地组件来调度。这让我们的业务代码极其清爽（就像拼接乐高积木一样），日后如果想换回本地模型，也只需替换这一块积木，其他的 RAG 代码一行都不用改！

```py
from langchain_core.documents import BaseDocumentCompressor, Document
from pydantic import Field
import requests
from typing import Sequence, Optional, Any


class SiliconFlowReranker(BaseDocumentCompressor):
    # 使用 Pydantic 定义组件的参数
    api_key: str = Field(description="你的 SiliconFlow API Key")
    # 重排模型
    model: str = Field(default="Qwen/Qwen3-Reranker-8B")
    top_n: int = Field(default=1)

    def compress_documents(
            self,
            documents: Sequence[Document],
            query: str,
            callbacks: Optional[Any] = None,
    ) -> Sequence[Document]:
        if not documents:
            return []

        # 1. 把文档提取成纯文本列表
        texts = [doc.page_content for doc in documents]

        # 2. 组装 JSON 负载，发送请求给硅基流动 API
        url = "https://api.siliconflow.cn/v1/rerank"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "query": query,
            "documents": texts,
            "top_n": self.top_n
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print("\n" + "!" * 50)
            print(f"❌ 硅基流动 API 拒绝了请求！状态码: {response.status_code}")
            print(f"📄 真实报错详情: {response.text}")
            print(f"📤 我们发送的 Payload: {payload}")
            print("!" * 50 + "\n")
        response.raise_for_status()  # 如果网络或 API 报错，直接抛出异常

        # 3. 解析云端模型给出的打分
        results = response.json().get("results", [])

        # 4. 根据返回的索引，把原文档挑出来，并附上云端给的分数
        final_docs = []
        for res in results:
            idx = res["index"]
            score = res["relevance_score"]
            doc = documents[idx]
            doc.metadata["relevance_score"] = score  # 记录下这珍贵的分数
            final_docs.append(doc)

        return final_docs
```

### 4. 最终代码

```py
import os
import json
import redis

import env_setup

from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_classic.retrievers import ParentDocumentRetriever, EnsembleRetriever, ContextualCompressionRetriever
from langchain_classic.storage import EncoderBackedStore

from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore

from langchain_community.storage import RedisStore

# 🌟 引入你手写的云端重排组件
from silicon_flow_components import SiliconFlowReranker

# ==========================================
# 1. 业务数据加载 & Markdown 语义切分
# ==========================================
print("1. 正在读取 parsed_result.md 并进行语义层级切分...")
with open("parsed_result.md", "r", encoding="utf-8") as f:
    markdown_document = f.read()

headers_to_split_on = [("#", "Header1"), ("##", "Header2"), ("###", "Header3")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
parent_docs = markdown_splitter.split_text(markdown_document)
print(f"-> 成功提取 {len(parent_docs)} 个自带层级 Metadata 的父文档。")

# ==========================================
# 2. 初始化核心基础设施 (Embedding, Redis, Qdrant)
# ==========================================
VECTOR_DIMENSION = 512

print("\n2. 初始化云端 Embedding (MRL 套娃降维至 512)...")
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B",
    dimensions=VECTOR_DIMENSION
)

print("3. 连接并初始化 Redis 与 Qdrant...")
# --- Redis: 存储庞大的大块文本 ---
redis_client = redis.Redis.from_url("redis://localhost:6379/0")
redis_byte_store = RedisStore(client=redis_client, namespace="rag:ultimate_kb:")


def encode_doc(doc: Document) -> bytes:
    return json.dumps({"page_content": doc.page_content, "metadata": doc.metadata}).encode("utf-8")


def decode_doc(b: bytes) -> Document:
    data = json.loads(b.decode("utf-8"))
    return Document(page_content=data["page_content"], metadata=data.get("metadata", {}))


store = EncoderBackedStore(
    store=redis_byte_store, key_encoder=lambda x: x, value_serializer=encode_doc, value_deserializer=decode_doc
)

# --- Qdrant: 存储 512 维的高密度向量 ---
qdrant_client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "company_ultimate_kb"

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
# 4. 构建双路召回网络 (带有底层标量过滤)
# ==========================================
print("\n4. 正在构建双路召回大炮...")

# 🚨 开启底层标量权限过滤
# 注意：运行前请确保这里的 "考勤与休假制度" 在你的 md 文件里真实存在，否则会什么都搜不到！
target_section = "考勤与休假制度"  # 请根据真实 Markdown 结构修改
strict_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="metadata.Header1",
            match=models.MatchValue(value=target_section)
        )
    ]
)

# A路：语义召回 (Qdrant + Redis + Filter)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=None,
    search_kwargs={"k": 3, "filter": strict_filter}  # 带着过滤条件找 Top 3
)

print("-> 正在将文本灌入双数据库 (Qdrant + Redis)...")
parent_retriever.add_documents(parent_docs)

# B路：关键词召回 (BM25)
# 为了保证 BM25 也严格遵守权限隔离，我们只把符合条件的文档喂给它建索引
filtered_parent_docs = [d for d in parent_docs if d.metadata.get("Header1") == target_section]
if not filtered_parent_docs:
    print(f"⚠️ 警告：未找到任何属于 [{target_section}] 的文档，BM25 将无数据可搜！")

bm25_retriever = BM25Retriever.from_documents(filtered_parent_docs if filtered_parent_docs else parent_docs)
bm25_retriever.k = 2

# 双路融合
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, parent_retriever],
    weights=[0.4, 0.6]  # 语义为主，关键词为辅
)

# ==========================================
# 5. 挂载 Qwen3-8B 云端重排副总裁
# ==========================================
print("\n5. 挂载云端 Qwen3-8B 重排副总裁...")
compressor = SiliconFlowReranker(
    api_key=os.environ.get("API_KEY"),
    model="Qwen/Qwen3-Reranker-8B",
    top_n=1  # 几十个候选里，我只要那极其精准的 1 个！
)

ultimate_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=ensemble_retriever
)

# ================= 见证最终奇迹 =================
print("\n" + "=" * 50)
query = "请假需要走什么流程？"

print(f"🔍 核心提问: {query}")
print("🧠 触发 [底层权限过滤 -> BM25+向量双路召回 -> Redis回表 -> 云端8B重排] 工业级流水线...")

retrieved_docs = ultimate_retriever.invoke(query)

print("\n🏆 【终极精准打分结果】:")
if not retrieved_docs:
    print("-> 🈳 过滤太严或无此内容。")
else:
    for doc in retrieved_docs:
        print(f"[{doc.metadata.get('relevance_score', 'N/A')}分] 所属章节: {doc.metadata}")
        print(f"【大段落原文】: \n{doc.page_content}\n")
print("=" * 50)
```
