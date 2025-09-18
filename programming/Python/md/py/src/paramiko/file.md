# 文件传输

```py
import paramiko

# 先建立 SSH 传输通道
transport = paramiko.Transport(("192.168.1.100", 22))
transport.connect(
    username="your_username",
    password="your_password"  # 也可使用 pkey=private_key 密钥登录
)

# 创建 SFTP 客户端对象
sftp = paramiko.SFTPClient.from_transport(transport)

try:
    # 场景 A：本地文件上传到服务器
    local_file_path = "/local/path/to/file.txt"  # 本地文件路径
    remote_file_path = "/remote/path/to/save/file.txt"  # 服务器保存路径
    sftp.put(local_file_path, remote_file_path)
    print(f"文件 {local_file_path} 上传成功")

    # 场景 B：从服务器下载文件到本地
    remote_download_path = "/remote/path/to/download/file.txt"  # 服务器文件路径
    local_save_path = "/local/path/to/save/downloaded.txt"  # 本地保存路径
    sftp.get(remote_download_path, local_save_path)
    print(f"文件 {remote_download_path} 下载成功")

finally:
    # 关闭 SFTP 和传输通道
    sftp.close()
    transport.close()
```
