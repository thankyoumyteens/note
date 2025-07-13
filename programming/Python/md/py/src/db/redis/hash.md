# 哈希操作

```py
# 设置哈希字段
connection.hset('user:1', 'name', 'Bob')
connection.hset('user:1', 'age', 30)
# 获取哈希字段的值
name = connection.hget('user:1', 'name')
print(f"HGET user:1 name: {name}")
# 获取所有哈希字段和值
hgetall = connection.hgetall('user:1')
print(f"HGETALL user:1: {hgetall}")
```
