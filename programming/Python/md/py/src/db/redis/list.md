# 列表操作

```py
# 从右侧添加元素（栈：右侧进右侧出）
connection.rpush('fruits', 'apple', 'banana', 'cherry')

# 从左侧添加元素
connection.lpush('fruits', 'orange')  # 此时列表：['orange', 'apple', 'banana', 'cherry']

# 获取列表长度
print(connection.llen('fruits'))  # 输出：4

# 获取指定范围的元素（0为第一个，-1为最后一个）
print(connection.lrange('fruits', 0, 2))  # 输出：['orange', 'apple', 'banana']

# 从右侧弹出元素（移除并返回）
print(connection.rpop('fruits'))  # 输出：cherry（列表剩余：['orange', 'apple', 'banana']）

# 从左侧弹出元素
print(connection.lpop('fruits'))  # 输出：orange（列表剩余：['apple', 'banana']）

# 根据索引修改元素
connection.lset('fruits', 0, 'grape')  # 列表变为：['grape', 'banana']
```
