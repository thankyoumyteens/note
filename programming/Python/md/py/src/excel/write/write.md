# Excel 写

```py
from openpyxl import Workbook

wb = Workbook()

# 获取正在使用的sheet
# 每次新建一个工作簿会默认生成一个名称为Sheet1的工作表
active_sheet = wb.active

# 改变sheet的名字
active_sheet.title = 'Sheet100'

# 写入数据 方法1
active_sheet.cell(row=1, column=1, value='第1行第1列')
# 写入数据 方法2
active_sheet.cell(row=1, column=2).value = '第1行第2列'

# 保存到文件
wb.save('demo.xlsx')
wb.close()
```
