# 删除指定页

```py
# pip install PyPDF2

import PyPDF2

# 读取原始的PDF文件
pdf_reader = PyPDF2.PdfReader("original.pdf")

# 创建一个新的PdfFileWriter对象
pdf_writer = PyPDF2.PdfWriter()

# 指定要删除的页面索引
delete_pages = [0, 1, 2]

# 获取原始文件中的总页数
total_pages = len(pdf_reader.pages)
# 循环遍历每一页
for i in range(total_pages):
    # 如果当前页索引不在要删除的页面列表中，则保留该页
    if i not in delete_pages:
        # 获取当前页
        page = pdf_reader.pages[i]
        # 将当前页添加到pdf_writer
        pdf_writer.add_page(page)

# 创建一个新的PDF文件
with open("original_deleted.pdf", "wb") as f:
    # 将pdf_writer的内容写入到新的PDF文件中
    pdf_writer.write(f)

print(new_file)
```
