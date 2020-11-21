# 权限问题

写完的Python脚本必须用管理员权限运行，才能对注册表进行写操作。否则会报PermissionError异常
这个时候需要调用Windows的API，重新启动一遍程序 runas administrator，将原来的程序退出。

代码也很简单
```python
from __future__ import print_function
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # TODO
else:
    if sys.version_info[0] == 3:
        # python3
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        # python2
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
```

# API

- OpenKey(key, subKey)：打开一个键，第一个参数是常量，例如reg.HEKY_CURRENT_USER，已经被系统定义好。
- CloseKey(key)：关闭打开的键。
- EnumKey(key, index)：枚举所有的key。
- EnumValue(key, index)：枚举所有的value，有三个返回值：键值名，键值，键类型。
- CreateKey(key, sub_key)：创建一个新键，如果键存在就不会创建。
- SetValueEx(key, value_name, reserved, type, value)：给一个键值赋值，如果键不存在将会自动创建。
- SetValue(key, sub_key, type, value)：设置一个子键，并给予一个默认值value。
- DeleteKey(key, sub_key)：删除键

# 例子: 添加右键菜单

```python
# apkinstaller: 自定义的key
# 其中 * 代表所有文件, 可以换成下面的值
#   AllFileSystemObjects: 所有文件和文件夹
#   Folder: 所有文件夹
#   Directory\Background 空白处右击
with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\apkinstaller") as key:
    # 设置右键菜单名
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "APK Installer")
    # 设置右键菜单图标
    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "%USERPROFILE%\\ApkInstaller.ico")

with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"*\shell\apkinstaller\command") as key:
    # 设置右键菜单执行的命令
    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "C:\\adb\\adb.exe install \"%1\"")
```
