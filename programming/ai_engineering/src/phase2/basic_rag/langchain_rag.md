# 用 LangChain 搭建朴素 RAG

我们用 Python + LangChain + Chroma（本地轻量级向量库）+ OpenAI API 来跑通这六步。

### 1. 安装依赖

```sh
pip install langchain langchain-openai langchain-chroma chromadb tiktoken
```

### 2. 代码

请仔细看注释里的 1~6 步对应关系

```py
import os

import env_setup

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

SILICON_FLOW_API_KEY = os.environ.get("API_KEY")

# 假设你本地有一个 knowledge.txt 文件
# ==========================================
# 第一步：加载 (Load)
# ==========================================
print("1. 正在加载文档...")
loader = TextLoader("knowledge.txt", encoding="utf-8")
docs = loader.load()

# ==========================================
# 第二步：切分 (Split)
# ==========================================
print("2. 正在切分文本...")
# 使用基础的字符切分器。
# chunk_size 是每块的大小，chunk_overlap 是块与块之间重叠的字数（防止一句话被从中间生硬截断）
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(docs)
print(f"-> 文件被切分成了 {len(chunks)} 个块。")

# ==========================================
# 第三步 & 第四步：嵌入 (Embed) 与 存储 (Store)
# ==========================================

print("3 & 4. 正在加载 Embedding 模型并存入 Chroma 向量库...")
embeddings_model = OpenAIEmbeddings(
    openai_api_key=SILICON_FLOW_API_KEY,
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B"
)

# Chroma 会在内存中创建一个向量库，并自动调用 embeddings_model 把 chunks 变成向量存进去
vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings_model)

# ==========================================
# 第五步：检索 (Retrieve)
# ==========================================
print("5. 开始检索...")
# 将数据库转换为检索器，k=2 表示每次搜索返回最相关的 2 个文本块
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

user_question = "这份文档主要讲了什么内容？"  # 替换成你文档里的相关问题
retrieved_docs = retriever.invoke(user_question)

# ==========================================
# 第六步：生成 (Generate)
# ==========================================
print("6. 拼接 Prompt 并调用 LLM 生成回答...")
llm = ChatOpenAI(
    api_key=SILICON_FLOW_API_KEY,
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    temperature=0,
)

# 把检索到的两个文本块的内容拼在一起作为上下文
context = "\n---\n".join([doc.page_content for doc in retrieved_docs])

# 最朴素的 Prompt 模板：基于上下文回答问题
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

### 3. knowledge.txt 文件

请将以下内容复制，并保存为与你 Python 脚本同级目录下的 knowledge.txt 文件：

```
星辰科技有限公司（Starry Tech）2026版内部员工手册摘要

【第一章：公司愿景与价值观】
星辰科技成立于2020年，我们的核心使命是“用AI技术让生活更简单”。公司的核心价值观包含三点：客户第一、拥抱变化、极致执行。

【第二章：考勤与办公制度】
1. 工作时间：公司实行弹性工作制。标准工作时间为工作日 10:00 - 19:00，包含中午 1.5 小时的午休时间（12:00 - 13:30）。
2. 核心工作时间：无论如何弹性，所有员工必须在 11:00 - 16:00 期间保持在线或在工位，以确保团队协作沟通顺畅。
3. 迟到与早退：每月允许有 3 次、每次不超过 30 分钟的免责迟到。超出部分将按照每分钟 2 元扣除当月绩效。

【第三章：假期与福利】
1. 年假：试用期（3个月）通过后，每位全职员工即可获得每年 12 天的带薪年假。工作满3年后，年假增加至 15 天。
2. 病假：每人每月享有 1 天带薪病假。连续请病假超过 2 天的，需要提供三甲医院开具的病假证明。
3. 餐补与交通费：公司每月随工资发放 800 元餐饮补贴。若因项目加班超过晚上 21:30，可通过企业滴滴企业版直接打车回家，费用由公司全额企业支付，无需个人垫付。
4. 设备补贴：入职时公司统一配发 MacBook Pro 14寸（M3芯片）。若员工自带电脑办公，每月可申领 200 元设备折旧补贴。

【第四章：IT与信息安全】
1. 网络连接：访客请连接 Starry_Guest，员工手机与个人设备请连接 Starry_Mobile。办公电脑需连接 Starry_Corp_5G，该网络需使用员工个人的 LDAP 账号密码进行 802.1X 认证。
2. 代码安全：严禁将公司任何内部代码、API 密钥或客户数据上传至公共 GitHub、Pastebin 或任何非公司授权的第三方云盘。违者将面临立即解除劳动合同的处罚。
3. VPN使用：非办公区访问公司内网的 Gitlab 或 Jira 系统，必须使用公司统一配发的 GlobalProtect VPN 客户端，并配合手机动态令牌（MFA）登录。
```

### 4. 测试指南：如何验证你的 RAG 系统？

把代码里的 user_question 依次替换成以下几个问题，看看大模型是否能给出准确的回答：

- 难度 1：直接事实抽取
  - 测试问题：“公司每个月发多少钱的餐补？加班到几点可以打车？”
  - 预期效果：LLM 应该能准确说出 800 元和 21:30，这证明检索 (Retrieve) 和 生成 (Generate) 基本工作正常。
- 难度 2：逻辑组合与条件判断
  - 测试问题：“我是一个刚入职 1 年的新员工，我今年有几天年假？如果我连续生病休息了 3 天，需要准备什么材料？”
  - 预期效果：LLM 应该能结合上下文，判断出“不到3年所以是12天年假”，并且指出“超过2天需要三甲医院证明”。这证明模型理解了切分后的文本（Chunk）内容。
- 难度 3：抗幻觉测试（超出文档范围）
  - 测试问题：“公司的公积金缴纳比例是多少？”
  - 预期效果：由于文档里根本没有提公积金，一个合格的 RAG 系统的 LLM 应该乖乖回答“我不知道”或“文档中未提及”，而不是凭空捏造一个 7% 或 12%。
