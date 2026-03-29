# 语义分块

传统的 RecursiveCharacterTextSplitter 就像一个按刻度切肉的机器，每隔 500 克切一刀。而语义分块是一个智能雷达。它会先把文章里的每一句话都变成向量（Embedding），然后计算相邻两句话的“余弦相似度”。

- 如果前一句话在讲“餐补”，后一句话也在讲“餐补”，它们的向量距离很近，说明在同一个语义主题里，系统就不切断它们。
- 如果前一句话讲“餐补”，后一句话突然变成了“迟到扣钱”，向量距离突然拉大，系统就敏锐地发现 **“主题变了”**，于是立刻在这里切一刀。

优缺点对比：

- 优点：切出来的块逻辑极其自洽，简直完美。
- 缺点：非常耗费算力。在 ETL 数据清洗阶段，你需要频繁调用 Embedding 模型计算每一句话的相似度，速度比基础切分慢得多。

语义分块的底层算法通常包含以下 4 个步骤：

1. 碎化（Sentence Splitting）：先把整篇文章按照句号、叹号、问号，切成最基础的一句句话。
2. 向量化（Embedding）：把每一句话都丢给 Embedding 模型，变成高维向量（比如 512 维的浮点数组）。这一步是最耗时的。
3. 计算滑窗距离（Calculate Distances）：计算相邻两句话（或者相邻的几个句子窗口）的向量余弦距离。
   - 如果第 2 句接着第 1 句的话茬说，它们的向量距离可能只有 0.1。
   - 如果第 3 句突然换了一个全新的话题，它和第 2 句的向量距离可能突然飙升到 0.6。
4. 寻找断点（Find Breakpoints）：设定一个阈值（比如超过所有距离的 90% 分位数），只要两句话的距离超过这个阈值，就在这里“砍一刀”。

## 用代码见证“语义雷达”的威力

在 LangChain 中，语义分块目前还在 langchain-experimental（实验性功能）包里，因为业界还在不断优化它的算法。

### 1. 安装依赖

```sh
pip install langchain-experimental
```

### 2. 代码

我们故意准备一段“话题突变”的文本，看看它能不能精准地在话题切换的地方切开。

```py
import os

import env_setup

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# 1. 准备一段【话题突变】的测试文本
# 前面在讲公司愿景，中间突然变成打车报销，最后变成电脑密码配置。
# 注意：里面没有任何换行符和段落标识，完全是一坨纯文本！
text = """星辰科技成立于2020年，我们的核心使命是用AI技术让生活更简单。公司始终坚持客户第一的价值观，不断迭代我们的核心产品。关于员工的日常报销，若因项目加班超过晚上21:30，可通过企业滴滴直接打车回家，费用由公司全额支付。另外，每月随工资发放800元餐饮补贴。新员工入职后，办公电脑需连接Starry_Corp_5G网络，该网络必须使用个人LDAP账号进行认证，严禁将密码泄露给外来访客。"""

print("1. 加载 Embedding 模型 (充当语义雷达)...")
embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ.get("API_KEY"),
    openai_api_base="https://api.siliconflow.cn/v1",
    model="Qwen/Qwen3-Embedding-8B"
)

print("2. 初始化语义分块器...")
# standard_deviation（标准差）的意思是：“只要这句话偏离了全文主题 X 个标准差，就切开它”。
semantic_chunker = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="standard_deviation",
    # 阈值可以调，越高切得越少（块越大），越低切得越碎，通常设置在 1.0 到 1.5 之间
    breakpoint_threshold_amount=1.0,
    # 🌟 注意：默认只有遇到 “英文句号/问号/叹号 + 空格” 时，才算一句话结束
    # 需要注入中文分句正则表达式！告诉它遇到中文的。？！也切开
    sentence_split_regex=r"(?<=[。？！.?!])"
)

print("3. 开始进行语义切分...")
docs = semantic_chunker.create_documents([text])

print(f"\n✅ 成功切分为 {len(docs)} 个语义块：\n")
for i, doc in enumerate(docs):
    print(f"--- 语义块 {i + 1} ---")
    print(doc.page_content)
    print()
```

即便我们没有任何 `\n` 段落符，语义分块器通常也能精准地把它切成多块。

## 实战避坑建议：

### 不要对所有数据都用语义分块！

我们在“第二步（数据清洗）”中提取出来的、已经带有良好 `#` 标题的 Markdown 文档，直接使用 MarkdownHeaderTextSplitter + Recursive 结合，性价比是最高的。

只有遇到那种 **“一大坨没分段的纯文本（比如从老旧系统里导出来的无格式大字段）”** 时，再上语义分块这把“屠龙刀”。

### 警惕“过拟合”

千万不要为了某一段特定的文本，去死磕切分参数。

如果你为了让这段测试文本完美切成 3 块，把阈值调得非常低（比如 0.5）。那么等明天你接入了几十万字的真实业务文档时，你会发现雷达太敏感了，它会把完整的上下文切得稀碎（可能一两句话就切成一块），最终导致检索彻底崩溃。

最佳实践：在生产环境中，设定一个适中的阈值（如 1.0 或 1.2），接受偶尔的“切分不够完美”，然后通过接下来的“混合检索”技术来弥补！
