# 针对 Markdown 的智能切分方法

之前我们用的 RecursiveCharacterTextSplitter 是“物理切分”：它不管你内容讲的是什么，只要字数到了，就强行找个标点符号切断。这会导致一个致命问题：上下文丢失。

假设你的文档有一段内容：

```markdown
### 3. 餐补与交通费

公司每月随工资发放 800 元餐饮补贴。
```

如果切分时，“标题”和“正文”刚好被切到了两个不同的 Chunk（块）里，大模型拿到“公司每月随工资发放 800 元餐饮补贴”这句话时，它根本不知道这是哪个部门的规定，也不知道这属于“餐补”范畴。

MarkdownHeaderTextSplitter 的魔法在于：提取元数据（Metadata）。它会把当前段落隶属的所有父级标题，自动作为字典塞进这个 Chunk 的 Metadata 里。大模型不仅能看到正文，还能看到它的“血统”。

## 体验智能切分与 Metadata

```py
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 假设这是我们上一步从 PDF 里提取出来的完美 Markdown 文本
markdown_document = """
# 星辰科技有限公司2026版内部员工手册

## 第二章：考勤与办公制度
### 1. 工作时间
公司实行弹性工作制。标准工作时间为工作日 10:00 - 19:00。
### 2. 迟到与早退
每月允许有 3 次、每次不超过 30 分钟的免责迟到。

## 第三章：假期与福利
### 1. 年假
试用期（3个月）通过后，即可获得每年 12 天的带薪年假。
"""

# 1. 定义你想保留的标题层级，以及对应的 Metadata 字段名
# 意思是：遇到一个 #，就把后面的字存入 "章"；遇到 ##，存入 "节"
headers_to_split_on = [
    ("#", "文档大标题"),
    ("##", "章"),
    ("###", "节"),
]

# 2. 初始化切分器
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False  # 是否在正文中保留标题符号，推荐保留（False）
)

# 3. 执行切分
md_header_splits = markdown_splitter.split_text(markdown_document)

# 4. 打印结果，见证魔法时刻
print(f"✅ 成功切分为 {len(md_header_splits)} 个独立块。\n")

for i, chunk in enumerate(md_header_splits):
    print(f"--- Chunk {i + 1} ---")
    print(f"📄 正文内容: {chunk.page_content.strip()}")
    print(f"🏷️ 元数据 (Metadata): {chunk.metadata}")
    print()
```

运行后，你会发现“迟到与早退”这段文字的 metadata 里，清晰地记录了 `{'文档大标题': '星辰科技有限公司2026版内部员工手册', '章': '第二章：考勤与办公制度', '节': '2. 迟到与早退'}`。

这就是极其宝贵的结构化上下文！存入向量数据库后，哪怕单看这一小段文本，系统也绝对不会搞错它的背景。

## 组合使用

在真实的生产环境中，我们通常不会只用 MarkdownHeaderTextSplitter。

因为它只按标题切。如果“第一章”下面有整整 5000 字的纯文本，没有子标题，它就会把这 5000 字当成一个巨大的 Chunk 返回。这又超出了 LLM 的上下文限制或 Embedding 模型的最大长度（比如 512 个 Token）。

最佳实践：组合使用：

1. 先用 MarkdownHeaderTextSplitter 按标题拆分，提取出完美的 Metadata
2. 再把拆出来的结果，交给 RecursiveCharacterTextSplitter 进行长度控制。

就像是切披萨：先按口味切出大块（Markdown 切分），再把每一块切成能一口吃下的小块（递归字符切分），而且每一小块上都保留着它是哪种口味的标签（Metadata）。

代码写出来是这样的：

```py
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

markdown_document = """
# 星辰科技有限公司2026版内部员工手册

## 第二章：考勤与办公制度
### 1. 工作时间
公司实行弹性工作制。标准工作时间为工作日 10:00 - 19:00。
### 2. 迟到与早退
每月允许有 3 次、每次不超过 30 分钟的免责迟到。

## 第三章：假期与福利
### 1. 年假
试用期（3个月）通过后，即可获得每年 12 天的带薪年假。
"""

headers_to_split_on = [
    ("#", "文档大标题"),
    ("##", "章"),
    ("###", "节"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False  # 是否在正文中保留标题符号，推荐保留（False）
)

# 执行 Markdown 切分
md_header_splits = markdown_splitter.split_text(markdown_document)

# 引入我们熟悉的递归切分器限制长度
text_splitter = RecursiveCharacterTextSplitter(
    # 为了看到效果，这里把 chunk_size 设置小一些
    chunk_size=20, chunk_overlap=20
)

final_splits = text_splitter.split_documents(md_header_splits)

print(f"✅ 成功切分为 {len(final_splits)} 个独立块。\n")

for i, chunk in enumerate(final_splits):
    print(f"--- Chunk {i + 1} ---")
    print(f"📄 正文内容: {chunk.page_content.strip()}")
    print(f"🏷️ 元数据 (Metadata): {chunk.metadata}")
    print()
```

输出如下：

```
...
--- Chunk 13 ---
📄 正文内容: 试用期（3个月）通过后，即可获得每年
🏷️ 元数据 (Metadata): {'文档大标题': '星辰科技有限公司2026版内部员工手册', '章': '第三章：假期与福利', '节': '1. 年假'}

--- Chunk 14 ---
📄 正文内容: 12 天的带薪年假。
🏷️ 元数据 (Metadata): {'文档大标题': '星辰科技有限公司2026版内部员工手册', '章': '第三章：假期与福利', '节': '1. 年假'}
```
