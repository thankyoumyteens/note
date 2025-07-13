# 集合操作

```py
# 添加元素到集合
connection.sadd('fruits', 'apple')
connection.sadd('fruits', 'banana')
connection.sadd('fruits', 'apple')  # 重复元素会被忽略
# 获取集合所有元素
smembers = connection.smembers('fruits')
print(f"SINTER fruits: {smembers}")
```

## 有序集合操作

有序集合的每个元素包含两部分: 值, 分数

```py
# 添加元素到有序集合（值, 分数）
connection.zadd('scores', {'Alice': 95, 'Bob': 85, 'Charlie': 90})
# 获取有序集合所有元素（按分数升序）
zrange = connection.zrange('scores', 0, -1, withscores=True)
print(f"ZRANGE scores 0 -1 withscores: {zrange}")
```
