# 列表操作

```py
# 从左侧插入元素
connection.lpush('tasks', 'task1')
# 从右侧插入元素
connection.rpush('tasks', 'task2')
# 从右侧弹出元素
val = connection.rpop('tasks')
print(f"RPOP tasks: {val}")
# 获取列表所有元素
lrange = connection.lrange('tasks', 0, -1)
print(f"LRANGE tasks 0 -1: {lrange}")
```
