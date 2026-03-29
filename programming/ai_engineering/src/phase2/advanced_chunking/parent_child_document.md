# 父子文档拆分

可以把父子文档拆分（Parent-Child Document）完美映射为数据库中的“二级索引与回表查询”：

1. 我们用非常细粒度的字段（子块/Child Chunk）去建立高精度的向量索引。
2. 一旦命中这个细粒度索引，我们不直接把局部数据丢给前端，而是拿到主键 ID，去主表里 **“回表”**，把包含这条数据的完整大记录（父块/Parent Chunk）取出来，喂给大模型。

假设你的文档里有这样一段话：

```
“星辰科技的餐补制度：公司每月随工资发放 800 元餐饮补贴。此外，如果是周末加班，额外提供 50 元/天的补助。”
```

- 如果切块太大（比如 1000 字一段）：用户搜“周末加班补助多少钱”，因为这 1000 字里讲了考勤、绩效、年假等各种东西，“周末补助”的语义被稀释了，向量匹配的得分会很低，导致检索失败。
- 如果切块太小（比如按句话切，50 字一段）：检索非常精准，系统完美命中了“此外，如果是周末加班，额外提供 50 元/天的补助。”这句话。但是！你把这句话单拎出来喂给 LLM，LLM 根本不知道这是哪个公司的、什么前提下的补助，它没有上下文。

父子文档机制完美解决了这个悖论：它在底层把这段话切成一句一句存入向量库（保证检索高命中率），但在给大模型时，它会把这一整段（甚至整章）一起拿出来（保证上下文完整）。

## 最佳实践（Best Practice）

- 父文档（大块）：应该用 Markdown 标题来切分。因为“一整个章节”天然就是一个完整的知识上下文。
- 子文档（小块）：必须用 RecursiveCharacter 来按字数切分！为什么？因为有的 Markdown 章节可能只有 50 个字，但有的章节可能有 3000 个字。如果你不把 3000 字的章节继续用字数强行切碎，向量模型（通常最多只能吃 512 个 Token）直接就被撑爆报错了。

## 实现 Parent-Child Document Retriever

在 LangChain 中，实现这个功能需要配合一个额外的组件：文档存储（Document Store）。

- 向量数据库（Chroma）：用来存子块的向量，负责“搜索”。
- 文档存储（InMemoryStore/Redis 等）：用来存父块的原文，负责“回表”。

### 1. 安装依赖

```sh
pip install langchain langchain-chroma redis langchain_community
```

### 2. 代码

```py
import json
import os

import env_setup

import redis
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.storage import RedisStore
from langchain_core.documents import Document
from langchain_classic.storage import EncoderBackedStore

# ==========================================
# 纯文本加载与 Markdown 语义切分
# ==========================================
print("1. 正在读取并进行 Markdown 语义切分...")
# 直接把文件读成一整个大字符串
with open("parsed_result.md", "r", encoding="utf-8") as f:
    markdown_document = f.read()

# 定义你要按照哪些级别的标题来切分
headers_to_split_on = [
    ("#", "Header 1"),  # 一级标题，提取到 metadata 的 "Header 1" 字段
    ("##", "Header 2"),  # 二级标题
    ("###", "Header 3"),  # 三级标题
]

# 实例化 Markdown 切分器
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 🌟 关键点：这一步直接生成了带有精美 metadata 的“父文档”列表！
parent_docs = markdown_splitter.split_text(markdown_document)

# 打印一个看看效果
print(f"切分出了 {len(parent_docs)} 个语义父块。示例 Metadata: {parent_docs[0].metadata}")

# ==========================================
# 准备组件 (Embedding, 子切分器)
# ==========================================
print("加载 Embedding 模型...")
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B"
)

# 此时只需要一个子切分器！保证塞给 Chroma 的向量不超过模型上限，切得越细，匹配越准
child_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

# ==========================================
# 初始化底层的存储
# ==========================================
# 向量数据库：存小块 (Child)
vectorstore = Chroma(collection_name="split_parents", embedding_function=embeddings)

print("连接 Redis 数据库...")
redis_client = redis.Redis.from_url("redis://localhost:6379/0")
# 初始化 LangChain 的 Redis 字节存储器 (增加一个 namespace 防止和其他缓存冲突)
redis_byte_store = RedisStore(client=redis_client, namespace="rag:parent_docs:")


# 定义序列化和反序列化方法 (Redis 存取 JSON 字节，检索器需要 Document 对象)
def encode_doc(doc: Document) -> bytes:
    # 序列化：将 Document 对象转为 JSON 字节
    return json.dumps({
        "page_content": doc.page_content,
        "metadata": doc.metadata
    }).encode("utf-8")


def decode_doc(b: bytes) -> Document:
    # 反序列化：将 JSON 字节还原回 Document 对象
    data = json.loads(b.decode("utf-8"))
    return Document(page_content=data["page_content"], metadata=data.get("metadata", {}))


# 使用 EncoderBackedStore 将底层的字节存储“升级”为文档存储
store = EncoderBackedStore(
    store=redis_byte_store,
    key_encoder=lambda x: x,  # Redis 的 key 依然是字符串 uuid，不需要变
    value_serializer=encode_doc,  # 存入时触发
    value_deserializer=decode_doc  # 取出时触发
)

# ==========================================
# 组装并灌库：巧妙的参数传递
# ==========================================

print("正在构建父子索引并写入 Redis / Chroma...")
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    # 🌟 架构师的黑魔法：告诉 Retriever 不要再画蛇添足切分父文档了！
    parent_splitter=None,
)
# 把刚才用 Markdown 切好的 parent_docs 喂进去
retriever.add_documents(parent_docs)

# ================= 见证奇迹的时刻 =================

# 测试问题：极其细节的提问
query = "请假需要走什么流程？"

# 传统的底层向量检索（看看子块匹配到了什么）
print("\n--- 1. 底层向量库直接匹配到的【子块】（极其零碎） ---")
sub_docs = vectorstore.similarity_search(query, k=1)
for doc in sub_docs:
    print(doc.page_content)

# 经过父文档检索器封装后的结果（回表后的数据）
print("\n--- 2. ParentDocumentRetriever 最终返回的【父块】（上下文极其丰富） ---")
retrieved_docs = retriever.invoke(query)
for doc in retrieved_docs:
    print(doc.page_content)
```
