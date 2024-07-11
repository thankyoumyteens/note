# 替换

1. re.sub("abcd","m",str1) 将 str1 中的 abcd 全部替换为 m
2. re.sub("abcd","m",str1,2) 只替换前两个字符
3. re.sub("\d",func,str1) 用 func()函数的返回值替换

## 将字符串中的数字替换成%

写法 1:

```python
# 每个数字后面加三个!
import re
s = 'A23GG4HFD567GGG4846'
print(re.sub('(\d+?)', lambda m : m.group(1) + "!!!", s))
# A2!!!3!!!GG4!!!HFD5!!!6!!!7!!!GGG4!!!8!!!4!!!6!!!
```

写法 2:

```python
import re

def parse(matched):
    return matched.group(1) + "!!!"

s = 'A23GG4HFD567GGG4846'
print(re.sub('(\d+?)', parse, s))
```
