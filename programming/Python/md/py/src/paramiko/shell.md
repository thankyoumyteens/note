# 交互式 Shell

```py
import paramiko
import re

def run_dependent_commands(host, user, pwd):
    # 建立 SSH 连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=user, password=pwd, port=22)
    # 启动交互式 Shell
    shell = ssh.invoke_shell()
    shell.settimeout(10)  # 超时时间，避免阻塞
    # 初始化：设置编码（避免输出乱码）并清空初始缓冲区
    shell.send("export LANG=en_US.UTF-8\n")
    shell.recv(4096)  # 读取编码设置的输出，避免干扰后续结果

    try:
        # 执行命令
        cmd = "ls /tmp"
        shell.send(f"{cmd}\n")

        # 读取命令的完整输出
        cmd_output = ""
        while True:
            if shell.recv_ready():
                # 分块读取输出并拼接（解决大输出场景）
                chunk = shell.recv(4096).decode("utf-8", errors="ignore")
                cmd_output += chunk
            else:
                break
        print(f"输出:\n{cmd_output.strip()}\n")

    except Exception as e:
        print(f"命令执行失败: {str(e)}")
    finally:
        # 关闭连接
        shell.close()
        ssh.close()

if __name__ == "__main__":
    run_dependent_commands(
        host="目标IP",
        user="用户名",
        pwd="密码"
    )
```
