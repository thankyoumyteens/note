# excel 操作

## 读取 excel

```python
from openpyxl import load_workbook

# 打开excel
wb = load_workbook('demo.xlsx')

# 获取sheet
sheet = wb.get_sheet_by_name('Sheet1')

# 获取最大行与最大列
print(sheet.max_row)
print(sheet.max_column)

# 读取第1行第2列的值
cell = sheet.cell(row=1, column=2)

print(cell.value)
```

## 写入 excel

```python
from openpyxl import Workbook

wb = Workbook()

# 获取正在使用的sheet
# 每次新建一个工作簿会默认生成一个名称为Sheet1的工作表
active_sheet = wb.active

# 改变sheet的名字
active_sheet.title = 'Sheet1'

# 写入数据
active_sheet.cell(row = 1, column = 1, value = '第1行第1列')
# 另一种写法
active_sheet.cell(row=1, column=2).value = '第1行第2列'

# 保存到文件
wb.save('demo.xlsx')
wb.close()
```
