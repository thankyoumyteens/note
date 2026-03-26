# 解析 PDF

PDF 解析之所以是痛点中的痛点，是因为 PDF 本质上不是文本文档，而是“画板”。它记录的是“在坐标 `(x,y)` 处画一个字”，而不是“这是一段标题，下面是表格”。

### 1. 安装依赖

安装 Docling（它内部集成了视觉模型，所以安装包会稍微有点大，请耐心等待）：

```sh
pip install docling
```

### 2. 代码

你可以随便找一份你手头最复杂的 PDF（最好带有表格、双栏、各种各样的标题级别），命名为 test_document.pdf，然后运行以下代码：

[随便找了一个员工手册](https://image.cailianpress.com/admin/20190906/pdf/ppwKhGe0WmlA/%E5%91%98%E5%B7%A5%E6%89%8B%E5%86%8C.pdf)

```py
import time
from docling.document_converter import DocumentConverter

# 假设你的 PDF 文件名是这个
pdf_path = "test_document.pdf"
output_md_path = "parsed_result.md"

print(f"🚀 开始解析 PDF: {pdf_path}")
print("（如果文档较大或包含复杂表格，可能会耗时很久，请稍候...）")

start_time = time.time()

# 1. 初始化转换器
converter = DocumentConverter()

# 2. 执行转换
# 这一步 Docling 会在底层进行版面分析（Layout Analysis），识别出哪里是标题、哪里是表格
result = converter.convert(pdf_path)

# 3. 导出为 Markdown 格式
markdown_content = result.document.export_to_markdown()

# 4. 保存到本地文件，方便我们肉眼检查“清洗”效果
with open(output_md_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

end_time = time.time()

print(f"✅ 解析完成！耗时: {end_time - start_time:.2f} 秒")
print(f"📄 完美的 Markdown 结果已保存至: {output_md_path}")
print("\n--- 预览前 500 个字符 ---")
print(markdown_content[:500])
```

## 为什么一定要转成 Markdown

这涉及到了我们下一步的 **“切分（Split）策略”**：

- 保留层级结构：Markdown 里的 `#`、`##` 明确地标识了文档的层级（章、节）。这能帮我们在切块时，知道这段话属于哪个大标题下。
- 保全表格结构：纯文本切分会把表格切得支离破碎（比如把表头和数据分到了不同的块里）。而 Markdown 使用 `|---|---|` 格式保留了表格的二维语义，大模型可以直接读懂 Markdown 表格！
