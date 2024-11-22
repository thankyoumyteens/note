# 屏幕操作

```python
import pyautogui

# 获取屏幕尺寸
s = pyautogui.size()
print(s.width, s.height)

# 判断指定坐标 (x,y) 是否在屏幕内
b = pyautogui.onScreen(100, 200)
print(b)
```
