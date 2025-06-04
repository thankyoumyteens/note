# 读取 sheet

```py
from openpyxl import load_workbook

wb = load_workbook('demo.xlsx')

# 遍历每个sheet
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f'sheet名: {sheet_name}, sheet对象: {sheet}')

# 获取指定的sheet对象
sheet = wb['Sheet1']

# 获取这个sheet的最大行与最大列
print(sheet.max_row)
print(sheet.max_column)
```
