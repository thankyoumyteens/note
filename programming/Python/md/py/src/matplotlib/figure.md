# 创建画布

```py
import matplotlib.pyplot as plt
# 创建一个空白画布
fig = plt.figure()
```

figure 函数的参数:

- `figsize` 指定画布的大小，(宽度,高度)，单位为英寸
- `dpi` 指定绘图对象的分辨率，即每英寸多少个像素，默认值为 80
- `facecolor` 背景颜色
- `dgecolor` 边框颜色
- `frameon` 是否显示边框
