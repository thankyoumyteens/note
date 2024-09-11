# 随机数

## 生成 n 位随机数

```py
import random

length = 4 # n 位
rand = ''.join(str(random.choice(range(10))) for _ in range(length))
print(rand)
```

拆解如下:

```py
import random

length = 4

arr = []
for i in range(length):
    # 生成一个 [0, 10) 范围的随机数
    random_number = str(random.choice(range(10)))
    arr.append(random_number)

rand = ''.join(arr)
print(rand)
```
