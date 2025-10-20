# 字符串操作

```py
# 设置值
connection.set('username', 'bob')

# 获取值
print(connection.get('username'))  # 输出：bob

# 批量设置/获取
connection.mset({'a': 1, 'b': 2, 'c': 3})
print(connection.mget(['a', 'b', 'c']))  # 输出：[1, 2, 3]

# 追加字符串
connection.append('username', '_smith')  # username 变为 'bob_smith'
```
