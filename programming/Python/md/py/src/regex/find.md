# 查找

- re.match 正则表达式要从行首开始写, match 匹配到换行符为止
- re.search 匹配整个字符串, 遇到换行符不停止

```python
import re

str = 'name:zhangsan,age:17'

m = re.search('age:(\d{2})', str)
m.group(1)  # result: 17

m = re.match('age:(\d{2})', str)
m.group(1)  # result: m is None
```
