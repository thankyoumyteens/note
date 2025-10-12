# 获取 Windows 桌面的缩放比例

```py
import ctypes

def get_windows_scaling_factor():
    try:
        # 调用 Windows API 函数获取缩放比例
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()

        # 计算缩放比例
        return scaling_factor / 96.0

    except Exception as e:
        print("获取缩放比例时出错:", e)
        return None

# 调用函数获取 Windows 桌面的缩放比例
scaling_factor = get_windows_scaling_factor()
if scaling_factor is not None:
    print("Windows 桌面的缩放比例:", scaling_factor)
```
