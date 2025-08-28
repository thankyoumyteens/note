# 判断当前操作系统

有多种方法:

- sys.platform 提供简短的标识字符串
- os.name 提供更通用的分类（'nt' 表示 Windows，'posix' 表示类 Unix 系统）
- platform 模块提供最详细的系统信息，包括版本号等

## 使用 sys 模块

```py
import sys

# 获取操作系统名称
os_name = sys.platform

print(f"操作系统标识: {os_name}")

# 判断具体系统
if os_name.startswith('win'):
    print("当前系统是Windows")
elif os_name.startswith('linux'):
    print("当前系统是Linux")
elif os_name.startswith('darwin'):
    print("当前系统是macOS")
elif os_name.startswith('freebsd'):
    print("当前系统是FreeBSD")
else:
    print("未知操作系统")
```

## 使用 os 模块

```py
import os

# 获取环境变量中的系统信息
os_name = os.name

print(f"系统名称: {os_name}")

if os_name == 'nt':
    print("Windows系统")
elif os_name == 'posix':
    # posix包含Linux、macOS、Unix等
    import platform
    if platform.system() == 'Darwin':
        print("macOS系统")
    else:
        print("Linux或类Unix系统")
else:
    print("未知操作系统")
```

## 使用 platform 模块

```py
import platform

# 获取系统名称
system_name = platform.system()
print(f"系统名称: {system_name}")

# 获取详细版本信息
system_version = platform.version()
print(f"系统版本: {system_version}")

# 判断系统类型
if system_name == "Windows":
    print("运行在Windows系统上")
elif system_name == "Linux":
    print("运行在Linux系统上")
elif system_name == "Darwin":
    print("运行在macOS系统上")
else:
    print(f"运行在{system_name}系统上")
```
