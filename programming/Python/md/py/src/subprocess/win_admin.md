# Windows 系统以管理员身份执行命令

该脚本会先判断当前用户是否具有管理员权限，如果没有，则尝试获取管理员权限。

获取到权限后系统会重新运行该脚本, 再进入 if 使用 subprocess.run 执行指定的命令。

```py
import ctypes
import sys
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(cmd):
    if is_admin():
        subprocess.run(cmd, shell=True, check=True)
    else:
        # 请求管理员权限
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

if __name__ == '__main__':
    cmd = 'echo Hello, Admin!'
    run_as_admin(cmd)
```
