```python
# 将窗口设置为最前面一层
def focus_window(hw):
    shell = win32com.client.Dispatch("WScript.Shell")
    dll = CDLL("user32.dll")
    shell.SendKeys('%')
    dll.LockSetForegroundWindow(2)
    if dll.IsIconic(hw):
        win32gui.SendMessage(hw, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    dll.SetWindowPos(hw, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    dll.SetForegroundWindow(hw)
    dll.SetActiveWindow(hw)
```
