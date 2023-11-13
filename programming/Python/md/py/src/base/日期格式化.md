# 日期格式化

```python
from datetime import datetime
dt = datetime.now()
# 2015-03-08 23:30:42
print(dt.strftime('%Y-%m-%d %H:%M:%S'))
# 15-03-08 11:30:42 PM
print(dt.strftime('%y-%m-%d %I:%M:%S %p'))
print('今天是这周的第%s天 ' + dt.strftime('%w'))
print('今天是今年的第%s天 ' + dt.strftime('%j'))
print('本周是今年的第%s周 ' + dt.strftime('%U'))
print('今天是当月的第%s天 ' + dt.strftime('%d'))
```
