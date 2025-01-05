# 创建子图

subplot() 函数用于创建多个子图(即在一个图形窗口中显示多个图表)。它使得你可以轻松地组织和管理多个图表。

函数定义:

```py
plt.subplot(nrows, ncols, index, **kwargs)
```

- `nrows` 子图网格的行数
- `ncols` 子图网格的列数
- `index` 当前子图的索引, 从 1 开始计数

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 2 * np.pi, 400)
y1 = np.sin(x)
y2 = np.cos(x)

# 创建一个 2x1 的子图布局
# [  1  ]
# [  2  ]
plt.subplot(2, 1, 1)  # 选择第一个子图
plt.plot(x, y1)
plt.title('Sine Wave')

plt.subplot(2, 1, 2)  # 选择第二个子图
plt.plot(x, y2)
plt.title('Cosine Wave')

plt.tight_layout()  # 自动调整子图参数, 使之填充整个图形区域
plt.show()
```

## 简写形式

```py
plt.subplot(nrows_ncols_index)
```

其中 nrows_ncols_index 是一个三位整数, 前两位表示行数和列数, 第三位表示当前子图的索引。

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 2 * np.pi, 400)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.arcsin(np.sin(x))

# 创建一个 2x2 的子图布局
# [1][2]
# [3][4]
plt.subplot(221)
plt.plot(x, y1)
plt.title('Sine Wave')

plt.subplot(222)
plt.plot(x, y2)
plt.title('Cosine Wave')

plt.subplot(223)
plt.plot(x, y3)
plt.title('Tangent Wave')

plt.subplot(224)
plt.plot(x, y4)
plt.title('Arcsine Wave')

plt.tight_layout()
plt.show()
```
