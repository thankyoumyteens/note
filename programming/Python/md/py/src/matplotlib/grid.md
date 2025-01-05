# 网格线

函数定义:

```py
plt.grid(b=None, which='major', axis='both', **kwargs)
```

- `b` 布尔值, 控制是否显示网格线。默认为 None, 即不改变当前状态
- `which` 指定要影响的刻度标签('major'、'minor' 或 'both')
- `axis` 指定哪个轴上显示网格线('both'、'x' 或 'y')
- `kwargs` 其他参数, 如颜色、线型等, 这些参数会被传递给 Line2D 对象来定义网格线的属性

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘制图形
plt.plot(x, y)

# 显示网格线
plt.grid(True)  # 等价于 plt.grid()

plt.show()
```

## 自定义网格线

```py
import matplotlib.pyplot as plt
import numpy as np

# 创建数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘制图形
plt.plot(x, y)

# 显示自定义的网格线
# 参数: 显示网格、颜色、线型、线宽
plt.grid(True, color='red', linestyle='--', linewidth=0.5)

plt.show()
```

linestyle 的可选值:

- `'-'` 或 `'solid'`：实线
- `'--'` 或 `'dashed'`：虚线
- `'-.'` 或 `'dashdot'`：点划线
- `':'` 或 `'dotted'`：点线
- `'None'` 或 `' '` 或 `''`：不绘制线条(仅显示标记)
