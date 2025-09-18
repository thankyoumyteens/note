# 密钥登录

```py
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 加载本地私钥文件（注意：私钥文件权限需设为 600，否则可能报错）
    private_key = paramiko.RSAKey.from_private_key_file("/path/to/your/private_key.pem")

    # 通过密钥连接服务器
    ssh.connect(
        hostname="192.168.1.100",
        port=22,
        username="your_username",
        pkey=private_key  # 指定私钥
    )

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command("ls -l /home")
    print(stdout.read().decode("utf-8"))

finally:
    ssh.close()
```
