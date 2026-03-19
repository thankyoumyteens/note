# 使用 RecursiveCharacterTextSplitter 切分文本

基础的 CharacterTextSplitter 有点“暴力”，它很容易把一句完整的话从中间劈开（比如把“星辰科”和“技有限公司”硬生生分在两个不同的文本块里），这会严重破坏上下文，导致检索极其不准。

而 RecursiveCharacterTextSplitter（递归字符切分器） 是目前 RAG 业界公认的最佳默认切分工具。

它内置了一组默认的分隔符降级策略：`["\n\n", "\n", " ", ""]`。

1. 它首先尝试用 `\n\n`（段落）来切分文本。
2. 如果切出来的某一段还是超过了你设置的 chunk_size，它就会“退一步”，用 `\n`（单行/句子）来切这一段。
3. 如果单行还是太长，再退一步用空格（词）切，最后才是强行按字符切。

结论：它能最大限度地保证一句话、一段话的语义完整性。

## 代码替换

```py
import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("1. 正在加载文档...")
loader = TextLoader("knowledge.txt", encoding="utf-8")
docs = loader.load()

# ==========================================
# 第二步：切分 (Split) 🌟 这里换成了 RecursiveCharacterTextSplitter
# ==========================================
print("2. 正在进行智能递归切分...")
text_splitter = RecursiveCharacterTextSplitter(
    # 你可以显式指定切分顺序，也可以不写（默认就是下面这个）
    separators=["\n\n", "\n", " ", ""],
    chunk_size=200,
    chunk_overlap=50,
    length_function=len  # 使用 Python 内置的 len 函数计算长度
)
chunks = text_splitter.split_documents(docs)
print(f"-> 文件被更合理地切分成了 {len(chunks)} 个块。")

# （可选）打印出前两个块看看效果，你会发现语句比之前完整多了
# print(chunks[0].page_content)
# print("---")
# print(chunks[1].page_content)

# ==========================================
# 第三步 & 第四步：嵌入 (Embed) 与 存储 (Store)
# ==========================================

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
print("3 & 4. 正在加载本地 Embedding 模型并存入 Chroma 向量库 (首次运行会自动下载，约 100MB，请耐心等待)...")
embeddings_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings_model)

print("5. 开始检索...")
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

user_question = "我是一个刚入职 1 年的新员工，我今年有几天年假？如果我连续生病休息了 3 天，需要准备什么材料？"
retrieved_docs = retriever.invoke(user_question)

DOUBAO_API_KEY = os.environ.get("OPENAI_API_KEY")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
LLM_ENDPOINT_ID = os.environ.get("ENDPOINT_ID")
print("6. 拼接 Prompt 并调用 LLM 生成回答...")
llm = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model=LLM_ENDPOINT_ID,
    temperature=0
)

context = "\n---\n".join([doc.page_content for doc in retrieved_docs])

prompt = f"""
你是一个专业的问答助手。请严格基于以下<已知上下文>来回答用户的问题。
如果上下文中找不到答案，请直接说"我不知道"，不要编造。

<已知上下文>:
{context}

问题: {user_question}
"""

response = llm.invoke(prompt)

print("\n🤖 AI 回答:")
print(response.content)
```
