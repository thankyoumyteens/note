# 替换

写法 1:

```py
import re

s = '2021-01-01'
# 通过 反斜杠+数字 来引用匹配到的组
s = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\1年\2月\3日', s)
print(s)
```

写法 2:

```py
import re


def replace_date(match):
    year, month, day = match.groups()
    return f'{year}年{month}月{day}日'


s = '2021-01-01'
s = re.sub(r'(\d{4})-(\d{2})-(\d{2})', replace_date, s)
print(s)
```
