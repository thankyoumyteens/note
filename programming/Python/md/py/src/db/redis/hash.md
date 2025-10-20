# 哈希操作

```py
# 设置哈希字段（单个）
connection.hset('user:100', 'name', 'Alice')
connection.hset('user:100', 'age', 30)

# 批量设置哈希字段
connection.hset('user:101', mapping={
    'name': 'Bob',
    'age': 25,
    'city': 'Shanghai'
})

# 获取哈希中单个字段
print(connection.hget('user:100', 'name'))  # 输出：Alice

# 获取哈希中所有字段和值
print(connection.hgetall('user:101'))  # 输出：{'name': 'Bob', 'age': '25', 'city': 'Shanghai'}

# 获取所有字段名
print(connection.hkeys('user:101'))  # 输出：['name', 'age', 'city']

# 获取所有字段值
print(connection.hvals('user:101'))  # 输出：['Bob', '25', 'Shanghai']

# 判断字段是否存在
print(connection.hexists('user:100', 'age'))  # 输出：True

# 删除哈希中的字段
connection.hdel('user:101', 'city')
```
