# macOS 环境下自动提权与特权端口绑定

**文档版本：** V1.0
**适用环境：** macOS、IDE 虚拟控制台（PyCharm / VSCode 等）
**核心目标：** 解决本地开发时，Python 脚本绑定 80 等特权端口（0-1023）触发的权限拦截问题，实现 IDE 内一键无感提权，并完美保留 `stdin/stdout` 标准流以支持交互式输入。

---

## 一、 背景与痛点分析

在 macOS/Linux 等类 Unix 系统中，绑定 80 端口需要 `root` 权限。如果在 IDE 中直接运行代码，会面临以下痛点：

1. **IDE 伪终端限制：** 传统的 `sudo` 会在终端请求密码，而 IDE 的运行控制台缺少真实的 TTY，导致直接抛出 `a terminal is required` 异常。
2. **安全软件拦截：** 使用 AppleScript (`osascript`) 唤起原生 GUI 密码框易被企业级安全软件（如 Jamf）判定为危险行为。
3. **标准流污染：** 若通过 `subprocess.PIPE` 强行向 `sudo` 注入密码，会切断子进程的 `stdin`，导致后续业务代码中的 `input()` 交互函数卡死。

## 二、 核心操作流程

### 1. 权限自检与交互提权

脚本启动时，需优先校验当前 UID：

- 若 `os.geteuid() == 0`，表明已有 root 权限，跳过此阶段。
- 若非 0，则通过 `getpass` 模块在 IDE 控制台中安全获取用户的 Mac 锁屏密码，并暂存至系统环境变量。

### 2. 注入 Askpass 并拉起子进程

- 利用 `tempfile` 动态生成一个包含获取环境变量逻辑的临时 Python 脚本。
- 将该脚本的绝对路径写入 `SUDO_ASKPASS` 环境变量。
- 携带 `-A` 参数执行 `sudo` 命令，通过 `subprocess.Popen` 拉起新的子进程（即提权后的自身）。

### 3. 环境清理与业务执行

- 子进程启动后（此时已具备 root 权限），执行 `lsof` 与 `kill -9` 强行释放被系统后台（如内置 Apache `httpd`）占用的 80 端口。
- 端口释放完毕后，执行核心业务（如 Paramiko SSH 隧道建立），并与用户进行正常的 CLI 交互。

### 4. 资源销毁（阅后即焚）

- 父进程挂起等待子进程结束。无论子进程正常结束还是异常中断，父进程的 `finally` 块必须销毁临时的 Askpass 脚本，并清除环境变量中的明文密码，确保系统安全。

---

## 三、 关键技术栈与实现原理

为了实现上述流程，此方案综合运用了以下系统级技术点：

### 1. 提权黑魔法：`SUDO_ASKPASS` 与 `sudo -A`

- **原理：** 绕过 TTY 限制的核心技术。`sudo -A` 参数指示操作系统不要向标准控制台请求密码，而是去执行环境变量 `SUDO_ASKPASS` 所指向的可执行文件，并将该文件的标准输出（stdout）作为密码读取。
- **优势：** 避免了与 IDE 虚拟控制台的底层冲突，也不会触发安全软件的 GUI 拦截警报。

### 2. 进程嵌套与重定向（`subprocess`）

- **原理：** 将 Python 脚本作为“启动器（父进程）”和“业务载体（子进程）”双重使用。父进程通过 `subprocess.Popen(..., sys.executable, ... sys.argv)` 携带提权参数重新拉起自身。
- **技术关键点：** 实例化 `Popen` 时**不指定** `stdin`, `stdout`, `stderr`，让子进程完美继承父进程的系统文件描述符。彻底解耦标准流，恢复业务代码中 `input()` 函数的阻塞读取能力。

### 3. 输出缓冲控制（Unbuffered I/O）

- **原理：** 解决 IDE 环境下子进程日志假死的问题。
- **技术关键点：** 在 `subprocess` 构建命令时注入 `-u` 参数（`python -u script.py`），强制 Python 解释器关闭标准输出的块缓冲机制，实现日志的实时刷入。

### 4. 终端控制序列（ANSI Escape Codes）

- **原理：** 消除 macOS `sudo` 底层强制输出的 `Password:` 提示符。
- **技术关键点：** 业务就绪打印前，使用 `\033[1A`（光标上移）与 `\033[2K`（清空当前行）对控制台进行覆写，保持输出界面的绝对整洁。

---

## 四、 标准代码模板

开发者可直接将以下骨架集成至项目中，在 `run_core_business()` 中填入业务逻辑即可：

```python
import os
import sys
import subprocess
import getpass
import tempfile
import stat
import time

def ensure_root_and_bypass_tty():
    """提权与终端隔离核心逻辑"""
    if os.geteuid() == 0:
        return

    print("🛡️ 检测到非 root 权限，准备绑定特权端口。", flush=True)
    password = getpass.getpass("请输入 Mac 锁屏密码以便提权: ")

    # 动态生成 Askpass 辅助脚本
    fd, askpass_path = tempfile.mkstemp(suffix=".py")
    with open(fd, 'w') as f:
        f.write(f"#!{sys.executable}\n"
                "import os\n"
                "print(os.environ.get('SUDO_PASS_TEMP', ''))\n")
    os.chmod(askpass_path, stat.S_IRWXU)

    # 注入环境变量
    os.environ['SUDO_PASS_TEMP'] = password
    os.environ['SUDO_ASKPASS'] = askpass_path

    # 组装提权命令，携带 -u 避免日志假死
    args = ["sudo", "-A", sys.executable, "-u"] + sys.argv

    try:
        # 拉起提权后的子进程，不劫持标准流
        process = subprocess.Popen(args)
        process.wait()
        sys.exit(process.returncode)
    except KeyboardInterrupt:
        print("\n👋 父进程已退出", flush=True)
        sys.exit(0)
    finally:
        # 阅后即焚安全机制
        if os.path.exists(askpass_path):
            os.remove(askpass_path)
        if 'SUDO_PASS_TEMP' in os.environ:
            del os.environ['SUDO_PASS_TEMP']

def release_privileged_port(port=80):
    """清理端口占用（如内置 httpd）"""
    try:
        result = subprocess.run(['lsof', '-t', f'-i:{port}'], capture_output=True, text=True)
        for pid in result.stdout.strip().split('\n'):
            if pid:
                subprocess.run(['kill', '-9', pid])
        time.sleep(1)
    except Exception:
        pass

def run_core_business():
    """实际业务载体"""
    print("\033[1A\033[2K\r🚀 权限就绪！端口已接管，环境初始化完成。", flush=True)

    # TODO: 在此处编写 Paramiko 隧道或其他需特权端口的代码

    try:
        while True:
            # 此时 stdin 畅通，可正常使用 input
            user_cmd = input("请输入控制指令: ")
            print(f"收到指令: {user_cmd}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 业务进程已安全关闭", flush=True)

if __name__ == '__main__':
    ensure_root_and_bypass_tty()
    release_privileged_port(80)
    run_core_business()
```
