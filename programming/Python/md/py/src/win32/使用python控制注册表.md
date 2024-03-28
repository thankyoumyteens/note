# 安装依赖
```
pip install pywin32
```

# 权限问题

写完的Python脚本必须用管理员权限运行, 才能对注册表进行写操作。否则会报PermissionError异常
这个时候需要调用Windows的API, 重新启动一遍程序 runas administrator, 将原来的程序退出。

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
    #
else:
    if sys.version_info[0] == 3:
        # python3
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        # python2
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
```

# Windows注册表基本项

项名|描述
-|-
HKEY_CLASSES_ROOT|是HKEY_LOCAL_MACHINE\Software 的子项, 保存打开文件所对应的应用程序信息
HKEY_CURRENT_USER|是HKEY_USERS的子项, 保存当前用户的配置信息
HKEY_LOCAL_MACHINE|保存计算机的配置信息, 针对所有用户
HKEY_USERS|保存计算机上的所有以活动方式加载的用户配置文件
HKEY_CURRENT_CONFIG|保存计算机的硬件配置文件信息

# 打开注册表

- RegOpenKey(key, subkey, reserved, sam)
- RegOpenKeyEx(key, subkey, reserved, sam)

两个函数的参数一样。参数含义如下: 

- Key: 必须为Windows注册表基本项。
- SubKey: 要打开的子项。
- Reserved: 必须为0。
- Sam: 对打开的子项进行的操作, 包括win32con.KEY_ALL_ACCESS、win32con.KEY_READ、win32con.KEY_WRITE等

例子
```python
key ＝ win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software',0,win32con.KEY_READ)
print(key)
```

# 关闭注册表

- RegCloseKey(key)

其参数只有一个, 其含义如下: 

- Key: 已经打开的注册表项的句柄。

例子
```python
win32api.RegCloseKey(key)
```

# 读取项值

- RegQueryValue(key, subKey) 读取项的默认值
- RegQueryValueEx(key, valueName) 读取某一项值

对于RegQueryValue, 其参数含义如下: 

- Key: 已打开的注册表项的句柄。
- subKey: 要操作的子项。

对于RegQueryValueEx, 其参数含义如下: 

- Key: 已经打开的注册表项的句柄。
- valueName: 要读取的项值名称。

例子
```python
import win32api
import win32con
# 打开"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer"项
key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
    'SOFTWARE\\Microsoft\\Internet Explorer',
    0, win32con.KEY_ALL_ACCESS)
# 读取项的默认值
print(win32api.RegQueryValue(key,''))
# 输出为空, 表示其默认值未设置
#读取项值名称为Version的项值数据, 也就是Internet Explorer的版本
print(win32api.RegQueryValueEx(key,'Version'))
# 输出('6.0.2900.2180', 1)
print(win32api.RegQueryInfoKey(key))  # RegQueryInfoKey函数查询项的基本信息
# 返回项的子项数目、项值数目, 以及最后一次修改时间
# 输出(26, 7, 128178812229687500L)   
```

# 设置项值

- RegSetValueEx(key, valueName, reserved, type, value) 要修改或重新设置注册表某一项的项值。如果项值存在, 则修改该项值, 如果不存在, 则添加该项值。
- RegSetValue(key, subKey, type, value) 设置项的默认值

对于RegSetValueEx, 其参数含义如下: 

- Key: 要设置的项的句柄。
- valueName: 要设置的项值名称。
- Reserved: 保留, 可以设为0。
- Type: 项值的类型。
- Value: 所要设置的值。

对于RegSetValue, 其参数含义如下: 

- Key: 已经打开的项的句柄。
- subKey: 所要设置的子项。
- Type: 项值的类型, 必须为win32con.REG_SZ。
- Value: 项值数据, 为字符串。

例子
```python
# 将"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer"
# 的默认值设为python
win32api.RegSetValue(key,'',win32con.REG_SZ,'python')
# 将其"Version"设置为7.0.2900.2180
win32api.RegSetValueEx(key,'Version',0,win32con.REG_SZ,'7.0.2900.2180')
```

# 添加、删除项

- RegCreateKey(key, subKey) 向注册表中添加项
- RegDeleteKey(key, subKey) 删除注册表中的项

其参数含义相同, 参数含义分别如下: 

- Key: 已经打开的注册表项的句柄。
- subKey: 所要操作(添加或删除)的子项。

例子
```python
# 向"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer"添加子项"Python"
win32api.RegCreateKey(key,'Python')
# 删除刚才创建的子项"Python"
win32api.RegDeleteKey(key,'Python')
```
