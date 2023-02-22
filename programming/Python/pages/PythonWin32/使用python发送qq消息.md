# 使用python发送qq消息

原理是先将需要发送的文本放到剪贴板中,
然后将剪贴板内容发送到qq窗口,
之后模拟按键发送enter键发送消息,
需要提前打开qq聊天窗口, 且不能最小化,
命令行窗口可以最小化

安装依赖
```
pip install pywin32
```

```python
import win32gui
from ctypes import CDLL

import win32con
import win32com.client
import win32clipboard as w
import time
import datetime
import random


def get_clipboard_text():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def set_clipboard_text(content):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, content)
    w.CloseClipboard()


def find_qq_window(window_name):
    # 获取qq窗口句柄
    handle_qq = win32gui.FindWindow('TXGuiFoundation', window_name)
    return handle_qq


def focus_self():
    hw = win32gui.FindWindow('ConsoleWindowClass', 'qq')
    # 将窗口设置为最前面一层
    shell = win32com.client.Dispatch("WScript.Shell")
    dll = CDLL("user32.dll")
    shell.SendKeys('%')
    dll.LockSetForegroundWindow(2)
    if dll.IsIconic(hw):
        win32gui.SendMessage(hw, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    dll.SetWindowPos(hw, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
    dll.SetForegroundWindow(hw)
    dll.SetActiveWindow(hw)


def send_qq_message(handle_qq, msg):
    # 将消息写到剪贴板
    set_clipboard_text(msg)
    focus_self()
    # 投递剪贴板消息到QQ窗体
    # WM_CHAR = 258
    # CTRL+V = 22
    win32gui.SendMessage(handle_qq, 258, 22, 2080193)
    # WM_PASTE = 770
    win32gui.SendMessage(handle_qq, 770, 0, 0)
    time.sleep(1)
    # 按下回车键
    win32gui.SendMessage(handle_qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(handle_qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


def send_msg(window_name):
    now = datetime.datetime.now()
    now_time = '{:0>4d}年{:0>2d}月{:0>2d}日'.format(now.year, now.month, now.day)
    now_hour = '{:0>2d}'.format(now.hour)
    msgs = ''
		handle_qq = find_qq_window(window_name)
		send_qq_message(handle_qq, msgs)


send_msg('')
```
