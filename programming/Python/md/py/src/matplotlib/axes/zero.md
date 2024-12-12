# 让刻度 0 落在原点上

手动设置坐标轴范围:

```py
fig = plt.figure()

ax_main = fig.add_axes((0.1, 0.1, 0.8, 0.8))

# 手动设置x轴范围
ax_main.set_xlim(left=0, right=10)
# 手动设置y轴范围
ax_main.set_ylim(bottom=0, top=20)
```
