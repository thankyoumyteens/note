# 删除指定页

```py
# pip install PyPDF2

import PyPDF2

# 读取原始的pdf文件
pdf_reader = PyPDF2.PdfReader("src.pdf")

# 用来生成新的pdf文件
pdf_writer = PyPDF2.PdfWriter()

# 指定要删除的页面索引
delete_pages = [0, 1, 2]

# 获取原始文件中的总页数
total_pages = len(pdf_reader.pages)
# 循环遍历每一页
for page_index in range(total_pages):
    # 如果当前页索引不在要删除的页面列表中，则保留该页
    if page_index not in delete_pages:
        # 获取当前页
        page = pdf_reader.pages[page_index]
        # 将要保留的页添加到pdf_writer
        pdf_writer.add_page(page)

# 将pdf_writer中的内容写入到新的pdf文件中
pdf_writer.write("dest.pdf")
```
