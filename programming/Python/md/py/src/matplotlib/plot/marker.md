# 设置数据点样式

marker 参数用于设置数据点的形状, 常用的值:

- `o`: 圆形
- `s`: 正方形
- `*`: 星号
- `x`: 叉号
- `D`: 菱形

例如:

```py
plt.plot(x, y, marker='*')
```

## 数据点的大小

markersize(或 ms) 用于指定数据点的大小, 是一个浮点数。

例如:

```py
plt.plot(x, y, markersize=10.0, marker='o')
```

## 数据点颜色

数据点的颜色默认和线条的颜色一致。

markeredgecolor(或 mec) 用于指定数据点边缘的颜色, markerfacecolor(或 mfc) 用于指定数据点的填充颜色, 它们可以接受颜色名称、RGB 或 RGBA 值、十六进制颜色代码。

例如:

```py
plt.plot(x, y, mfc='green', markersize=10.0, marker='o')
```
