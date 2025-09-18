# 密码登录

```py
import paramiko

# 创建 SSH 客户端对象
ssh = paramiko.SSHClient()
# 自动接受未知的主机密钥（首次连接时避免报错）
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 连接 SSH 服务器（IP、端口、用户名、密码）
    ssh.connect(
        hostname="192.168.1.100",  # 目标服务器 IP 或域名
        port=22,                   # SSH 默认端口 22
        username="your_username",  # 登录用户名
        password="your_password"   # 登录密码
    )

    # 执行远程命令（示例：查看服务器磁盘使用情况）
    stdin, stdout, stderr = ssh.exec_command("df -h")

    # 获取命令输出（stdout 为正确输出，stderr 为错误信息）
    print("命令执行结果：")
    print(stdout.read().decode("utf-8"))  # 解码为字符串并打印
    if stderr.read():
        print("错误信息：", stderr.read().decode("utf-8"))

finally:
    # 关闭连接
    ssh.close()
```
