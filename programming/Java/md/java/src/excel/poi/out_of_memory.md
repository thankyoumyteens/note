# 内存溢出问题

当数据量超出一定限制（如 65536 条）时, 使用 HSSFWorkbook(处理 xls) 或 XSSFWorkbook(处理 xlsx) 会一次性把整个 excel 都加载都内存中, 可能会报 OutOfMemoryError。

## 解决

使用 SXSSFWorkbook

SXSSFWorkbook 采用了流式写入的方式, 这意味着它不是一次性将整个 Excel 文件加载到内存中, 而是分批次地写入数据。
