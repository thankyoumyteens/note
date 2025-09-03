# 多显示器截图

使用 mss

```sh
pip install mss
```

注意: `sct.monitors` 是个列表, 索引 1 是第一块显示器, 索引 2 是第二块显示器, 索引 0 是两块显示器合并后的区域。

```py
import mss
import mss.tools


with mss.mss() as sct:
    # 获取第二个显示器的信息
    monitor_number = 2
    mon = sct.monitors[monitor_number]

    # 设置截图的区域
    monitor = {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor_number,
    }

    # 截图
    sct_img = sct.grab(monitor)
    # 可以把截图转成opencv格式
    # img = np.array(sct_img)

    # 保存图片
    mss.tools.to_png(sct_img.rgb, sct_img.size, output='1.png')
```
