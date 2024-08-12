# 简写

## if 简写

```py
True的逻辑 if 条件 else False的逻辑
```

例如

```py
# 简写
a = 10 if i > 1 else 100

# 还原
if i > 1:
    a = 10
else:
    a = 100
```

## for 简写

```py
[ 对i的操作 for i in 列表 ]
```

例如

```py
# 简写
arr = [ i + 1 for i in range(1, 10)]

# 还原
arr = []
for i in range(1, 10):
    arr.append(i + 1)
```

## lambda 表达式

```py
lambda 参数: 表达式
```
