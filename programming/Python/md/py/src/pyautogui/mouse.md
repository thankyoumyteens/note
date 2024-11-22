# 鼠标操作

```python
import pyautogui

# 获取鼠标当前坐标
p = pyautogui.position()
print(p.x, p.y)
```

## 移动

```py
# 以屏幕左上角为原点(0, 0), 在 3 秒内将鼠标移动到指定坐标: (100, 200)
pyautogui.moveTo(100, 200, duration=3)

# 以鼠标当前位置为原点(0, 0), 在 3 秒内将鼠标移动到指定坐标: (100, 200)
pyautogui.moveRel(100, 200, duration=3)
```

## 拖拽

```py
# 以屏幕左上角为原点(0, 0), 在 3 秒内将鼠标从当前位置拖动到指定坐标: (100, 200)
pyautogui.dragTo(100, 200, duration=3)

# 以鼠标当前位置为原点(0, 0), 在 3 秒内将鼠标从当前位置拖动到指定坐标: (100, 200)
pyautogui.dragRel(100, 200, duration=3)
```

## 点击

```py
# 鼠标在(x, y)位置进行点击

# 鼠标左键单击
pyautogui.leftClick(x=100, y=200)

# 鼠标右键单击
pyautogui.rightClick(x=100, y=200)

# 鼠标中键单击
pyautogui.middleClick(x=100, y=200)

# 双击
pyautogui.doubleClick(x=100, y=200)

# 左键按下
pyautogui.mouseDown(x=100, y=200, button='left')

# 左键抬起
pyautogui.mouseUp(x=100, y=200, button='left')

# clicks: 点击次数, 默认1次。传2时等于一次双击
# interval: 两次点击间隔时长, 默认0.0；大于1.0后。默认为点击一次
# duration: 所耗时长, 默认0.0。
pyautogui.click(x=100, y=200, clicks=2, interval=0.1, duration=3.0)
```

## 滚动

```py
# 向上滚动
pyautogui.scroll(50, x=100, y=200)

# 向下滚动
pyautogui.scroll(-50, x=100, y=200)
```
