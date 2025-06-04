# 获取合并单元格的值

```py
from openpyxl import load_workbook


def get_merged_cells_value(sheet, row_index, col_index):
    """
    判断单元格是否为合并单元格，是则返回合并单元格的值，否则返回None
    """
    merged_cells = sheet.merged_cells  # 获取所有合并的单元格
    for merged_cell_info in merged_cells:
        # 获取合并单元格的范围
        min_col, min_row, max_col, max_row = merged_cell_info.bounds
        # 检查单元格是否在合并的单元格范围内
        if min_row <= row_index <= max_row and min_col <= col_index <= max_col:
            return sheet.cell(row=min_row, column=min_col).value
    return None


# 使用示例
wb = load_workbook('demo.xlsx')
sheet = wb['Sheet1']
print(get_merged_cells_value(sheet, 17, 2))
```
