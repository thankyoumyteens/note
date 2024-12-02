# 创建坐标轴

函数定义:

```py
add_axes(rect, projection=None, polar=False, **kwargs)
```

- `rect` 一个元组 `(left, bottom, width, height)`，定义了新坐标轴在画布左下角的坐标(left, bottom)和宽高(取值范围 0 到 1, 是画布大小的百分比)
- `projection` 坐标轴的投影类型，常见的有 rectilinear（直角坐标）、polar（极坐标）
- `polar` 如果为 True，则创建一个极坐标轴

## 创建直角坐标

```py
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 2 * np.pi, 0.01)
# y = sin x
y = np.sin(x)

fig = plt.figure()

# 添加一个坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))

# 在坐标轴上绘图
ax_main.plot(x, y)

plt.show()
```

## 创建极坐标

```py
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2 * np.pi, 100)
# r = cos 2θ
r = np.cos(2 * theta)

fig = plt.figure()

# 添加一个坐标轴
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8), polar=True)

# 在坐标轴上绘图
ax_main.plot(theta, r)

plt.show()
```

## 在同一画布中创建多个坐标轴

```py
import matplotlib.pyplot as plt

# 创建一个新的图形
fig = plt.figure()

# 添加一个主坐标轴, 占据图形的大部分区域
ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))
ax_main.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax_main.set_title('Main Axes')

# 添加一个小的子坐标轴, 位于主坐标轴的左上角
ax_inset = fig.add_axes((0.2, 0.6, 0.2, 0.2))
ax_inset.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax_inset.set_title('Inset Axes')

plt.show()
```
