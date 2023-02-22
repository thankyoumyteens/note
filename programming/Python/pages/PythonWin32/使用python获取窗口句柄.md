# 通过名称查找
```python
hwnd = win32gui.FindWindow(class_name, window_name)
```

# 通过坐标查找
```python
pos = (0, 0)
hwnd = win32gui.WindowFromPoint(pos)
```

# 遍历当前屏幕上所有的父窗口
```python
def callback_function(hwnd, l_param):
    pass
win32gui.EnumWindows(callback_function, l_param)
```

## 根据句柄获取窗口信息
```python
class_name = win32gui.GetClassName(hwnd)
window_name = win32gui.GetWindowText(hwnd)
```

# 遍历父窗口下所有的子窗口
```python
def callback_function(hwnd, l_param):
    pass
win32gui.EnumChildWindows(hwnd, callback_function, l_param)
```

# 获取指定窗口的父窗口句柄
```python
parent_hwnd = win32gui.GetParent(hwnd)
```

# 使用GetWindow复杂查找
函数定义
```python
HWND win32gui.GetWindow(hWnd, nCmd)
```

nCmd 可选值:  
1. GW_HWNDFIRST = 0: 同级别第一个
2. GW_HWNDLAST = 1: 同级别最后一个
3. GW_HWNDNEXT = 2: 同级别下一个
4. GW_HWNDPREV = 3: 同级别上一个
5. GW_OWNER = 4: 所属的主窗口
6. GW_CHILD = 5: 子窗口

例子: 查找当前窗口的同级别下一个窗口
```python
hwnd_1 = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
```

# 根据进程Id查找
```python
def callback(hwnd, hwnds):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid:
            hwnds.append(hwnd)
        return True
def get_hwnds_for_pid(self,pid):
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    print hwnds
    return hwnds
```
