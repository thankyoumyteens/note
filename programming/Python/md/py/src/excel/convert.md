# 列号的字母数字转换

```python
from openpyxl.utils import get_column_letter, column_index_from_string

# 根据列的数字返回字母
print(get_column_letter(1))  # A

# 根据字母返回列的数字
print(column_index_from_string('C'))  # 3
```
