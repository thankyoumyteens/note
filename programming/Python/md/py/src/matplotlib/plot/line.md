# 设置线条样式

linestyle(或 ls) 用于设置线条样式, 常用的值:

- `solid` 或 `-`: 实线
- `dashed` 或 `--`: 虚线
- `dashdot` 或 `-.`: 点划线
- `dotted` 或 `:`: 点线
- `None`: 不绘制线条

例如:

```py
plt.plot(x, y, linestyle='dashdot')
```

## 设置线条宽度

linewidth(或 lw) 用于指定线条的宽度, 是一个浮点数。

```py
plt.plot(x, y, linewidth=10.0)
```

## 设置线条颜色

color 用于指定线条的颜色, 常用的值:

- r: 红色
- g: 绿色
- b: 蓝色
- c: 青色
- m: 品红
- y: 黄色
- k: 黑色
- w: 白色
- 使用 RGB: 例如 `color=(255, 0, 0)`
- 使用 RGBA: 例如 `color=(0, 255, 0, 0.5)`
- 使用十六进制: 例如 `color='#FFA500'`

例如:

```py
plt.plot(x, y, color='b')
```
