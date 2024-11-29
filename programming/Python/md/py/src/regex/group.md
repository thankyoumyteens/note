# 分组

```python
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m.group(0)) # 010-12345
print(m.group(1)) # 010
print(m.group(2)) # 12345
```

注意: group(0)永远是原始字符串, group(1), group(2)表示第 1, 2 个子串。

## 获取所有分组

注意: 不包括 group(0)

```python
t = '19:05:30'
m = re.match(r'^([0-9]{2})\:([0-9]{2})\:([0-9]{2})$', t)
print(m.groups()) # ('19', '05', '30')
```
