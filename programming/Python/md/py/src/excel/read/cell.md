# 读取单元格

```py
from openpyxl import load_workbook

wb = load_workbook('demo.xlsx')
sheet = wb['Sheet1']
```

## 遍历

```py
# 遍历每一行
for row in sheet.iter_rows():
    # 遍历每一列
    for cell in row:
        # 输出单元格的值
        print(cell.value, end='\t')
```

## 获取指定的单元格

```py
# 获取指定的单元格 方法1
cell_a1 = sheet['A1']
print(cell_a1.value)

# 获取指定的单元格 方法2
# 索引从1开始
cell_a1 = sheet.cell(row=1, column=1)
print(cell_a1.value)
```

## 获取某一行所有单元格

```py
# 获取第2行的所有单元格
for cell in sheet[2]:
    print(cell.value)

# 跳过第一列, 获取第2行的所有单元格
for col in sheet.iter_cols(min_row=2, max_row=2, min_col=2, max_col=sheet.max_column):
    print(col[0].value)
```

## 获取某一列所有单元格

```py
# 获取第2列的所有单元格
for cell in sheet['B']:
    print(cell.value)

# 跳过第一行, 获取第2列的所有单元格
for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=2, max_col=2):
    print(row[0].value)
```
