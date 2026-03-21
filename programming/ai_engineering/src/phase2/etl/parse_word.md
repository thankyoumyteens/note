# 解析 Word

解析 PDF 就像是逼着你用 OCR 去识别一张图片里的文字和表格；而解析 Word（.docx）本质上就是在解析一个 XML/DOM 树。

因为 .docx 文件实际上就是一个 ZIP 压缩包（你可以试着把 .docx 后缀改成 .zip 然后解压），里面装的全是按结构组织好的 XML 文件。它天生就知道什么是“标题 1”、什么是“正文”、什么是“表格”。

## 直接复用“神器” Docling

Docling 其实是一个多模态文档解析引擎。它不仅支持 PDF，还完美支持 .docx、.pptx、.html。

这意味着，你完全不需要改动上一节的核心代码，只需要把传入的文件路径从 .pdf 换成 .docx，它就能自动读取 Word 内部的 XML 结构，并原封不动地输出为我们需要的、带有 `#` 和 `|---|` 的完美 Markdown！

```py
from docling.document_converter import DocumentConverter

# 只要换一下文件名，你的 ETL 流水线就能无缝处理 Word 了！
word_path = "company_rules.docx"
output_md_path = "word_parsed_result.md"

converter = DocumentConverter()
# Docling 会自动识别这是 Word 文件，并提取其原生结构
result = converter.convert(word_path)

markdown_content = result.document.export_to_markdown()

print(markdown_content[:500])
```

## 使用 python-docx 进行底层精细控制

有时候，业务部门的需求会比较“刁钻”。比如：“我只要 Word 文档里标红的文字”，或者“我只需要提取出 Word 里的所有表格，正文不要”。

Docling 这种一键转 Markdown 的工具就显得不够灵活了。这时，你需要使用 Python 圈操作 Word 的底层标准库：python-docx。

### 1. 安装依赖

```sh
pip install python-docx
```

### 2. 实战代码

```py
from docx import Document

print("🚀 开始解析 Word 文档底层结构...")
# 加载 Word 文档
doc = Document("company_rules.docx")

# 1. 提取所有段落，并获取它的“样式”（这就是天然的 Metadata！）
print("\n--- 提取段落与标题 ---")
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text: # 过滤掉空行
        style_name = para.style.name
        # 你会看到类似 'Heading 1', 'Normal', 'List Paragraph' 等原生样式
        print(f"[样式: {style_name}] -> {text[:30]}...")

        # 💡 RAG 启发：如果你在这里发现 style_name 是 'Heading 1'，
        # 你就可以在代码里手动给接下来的文本打上 Metadata 标签！

# 2. 提取 Word 中的所有表格
print("\n--- 提取表格数据 ---")
for table_index, table in enumerate(doc.tables):
    print(f"\n找到第 {table_index + 1} 个表格：")
    for row in table.rows:
        # 提取每一行中所有单元格的文字
        row_data = [cell.text.strip() for cell in row.cells]
        print(" | ".join(row_data))
```

优势：精细到了细胞级别。你可以通过 para.runs 读取到某句话是否加粗、是否是斜体、字体颜色是什么。这在处理包含高亮重点的结构化业务合同（如法律文书审核）时极其有用。
