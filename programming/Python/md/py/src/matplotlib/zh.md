# 中文乱码

在脚本中设置:

```py
import matplotlib.pyplot as plt

# 设置中文字体
# 去 /System/Library/Fonts/ 中找一个中文字体
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 绘图示例
x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

plt.plot(x, y)
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('简单图表')
plt.show()
```

## 设置全局字体

### 1. 找到 Matplotlib 的配置文件 `matplotlibrc`：

```sh
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"
```

### 2. 编辑 `matplotlibrc` 文件，添加或修改以下行：

确保你的系统安装了这些字体。如果没有安装，可以从网上下载并安装合适的中文字体

```
font.family: sans-serif
font.sans-serif: SimHei, Arial Unicode MS
```
