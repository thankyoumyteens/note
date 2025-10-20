# 集合操作

```py
# 添加元素
connection.sadd('tags', 'python', 'java', 'c++')

# 获取集合所有元素
print(connection.smembers('tags'))  # 输出：{'python', 'java', 'c++'}（无序）

# 判断元素是否在集合中
print(connection.sismember('tags', 'python'))  # 输出：True

# 集合长度
print(connection.scard('tags'))  # 输出：3

# 删除元素
connection.srem('tags', 'c++')  # 集合剩余：{'python', 'java'}

# 交集（两个集合的共同元素）
connection.sadd('tags2', 'java', 'javascript', 'python')
print(connection.sinter('tags', 'tags2'))  # 输出：{'python', 'java'}

# 并集（两个集合的所有元素，去重）
print(connection.sunion('tags', 'tags2'))  # 输出：{'python', 'java', 'javascript'}
```

## 有序集合操作

有序集合的每个元素包含两部分: 值, 分数

```py
# 添加元素（值+分数）
connection.zadd('rank', {
    'Alice': 90,
    'Bob': 85,
    'Charlie': 95
})

# 按分数升序获取元素（0为第一个，-1为最后一个）
print(connection.zrange('rank', 0, -1, withscores=True))  # 带分数输出
# 输出：[('Bob', 85.0), ('Alice', 90.0), ('Charlie', 95.0)]

# 按分数降序获取元素
print(connection.zrevrange('rank', 0, -1, withscores=True))
# 输出：[('Charlie', 95.0), ('Alice', 90.0), ('Bob', 85.0)]

# 获取元素的分数
print(connection.zscore('rank', 'Alice'))  # 输出：90.0

# 增加元素分数
connection.zincrby('rank', 5, 'Bob')  # Bob的分数变为90

# 删除元素
connection.zrem('rank', 'Charlie')
```
