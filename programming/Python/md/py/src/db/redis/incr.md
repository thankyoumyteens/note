# 自增操作

```py
# 初始化计数器的值
connection.set('counter', 10)
# 自增
connection.incr('counter')
# 输出: 11
print(connection.get('counter'))
```
