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

## 屏幕缩放比例的影响

mss 获取的屏幕尺寸与实际不符（如偏大 1120px），通常与系统缩放（DPI 缩放）、虚拟桌面坐标计算方式或多显示器排列配置有关。mss 获取的是系统原始像素坐标，而现代操作系统（Windows/macOS）默认启用 DPI 缩放（如 125%、150%），导致实际物理尺寸与虚拟像素尺寸不一致。

例如：若显示器物理分辨率为 1920×1080，但系统缩放为 125%，系统会将其虚拟为 1536×864（1920/1.25=1536），但 mss 仍会按原始物理像素 1920×1080 计算，导致尺寸偏大。

可以在代码中通过具体操作系统的 API 获取缩放比例，修正尺寸。
