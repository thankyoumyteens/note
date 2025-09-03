# 获取输入法中英文状态

```py
import win32api, win32con, win32gui
import ctypes

IMC_GETOPENSTATUS = 0x0005
IMC_SETOPENSTATUS = 0x0006

imm32 = ctypes.WinDLL('imm32', use_last_error=True)
# 当前处在前台的进程窗口句柄
handle = win32gui.GetForegroundWindow()
hIME = imm32.ImmGetDefaultIMEWnd(handle)
# 返回值 0:英文 1:中文
status = win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_GETOPENSTATUS, 0)

if satus:
    print('中文')
else:
    print('英文')
```
