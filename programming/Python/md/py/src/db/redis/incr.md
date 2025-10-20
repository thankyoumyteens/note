# 自增操作

```py
# 初始化计数器的值
connection.set('counter', 10)

# 自增/自减（仅对数字有效）
connection.incr('a')  # a = 2
connection.decr('b')  # b = 1
connection.incrby('a', 5)  # a +=5 -> 7
connection.decrby('b', 3)  # b -=3 -> -2
```
