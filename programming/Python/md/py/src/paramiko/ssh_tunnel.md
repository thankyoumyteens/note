# 创建 SSH 隧道

```py
import paramiko
import threading
import socket
import time
import webbrowser
from typing import Optional


class WebSSHTunnel:
    def __init__(self,
                 ssh_host: str,
                 ssh_port: int = 22,
                 ssh_user: str = "",
                 ssh_password: Optional[str] = None,
                 ssh_key_path: Optional[str] = None,
                 local_port: int = 8080,
                 target_host: str = "",
                 target_port: int = 80):
        """
        初始化网页访问SSH隧道
        :param ssh_host: SSH服务器地址
        :param ssh_port: SSH服务器端口
        :param ssh_user: SSH登录用户名
        :param ssh_password: SSH密码（与密钥二选一）
        :param ssh_key_path: SSH私钥路径
        :param local_port: 本地映射端口
        :param target_host: 远程服务器地址
        :param target_port: 远程服务器端口
        """
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_key_path = ssh_key_path
        self.local_port = local_port
        self.target_host = target_host
        self.target_port = target_port

        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.transport: Optional[paramiko.Transport] = None
        self.listener: Optional[socket.socket] = None
        self.running = False

    def start(self) -> bool:
        """启动SSH隧道，返回是否成功"""
        try:
            # 初始化SSH客户端
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 准备认证参数
            auth_args = {}
            if self.ssh_key_path:
                auth_args['key_filename'] = self.ssh_key_path
            elif self.ssh_password:
                auth_args['password'] = self.ssh_password

            # 连接SSH服务器
            self.ssh_client.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_user, **auth_args
            )

            # 获取传输层
            self.transport = self.ssh_client.get_transport()
            if not self.transport:
                print("无法获取SSH传输层")
                return False

            # 创建本地监听套接字
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind(('localhost', self.local_port))
            self.listener.listen(5)  # 允许同时处理5个连接

            self.running = True
            print(f"SSH隧道已启动:")
            print(f"本地: localhost:{self.local_port}")
            print(f"映射到: {self.target_host}:{self.target_port}")

            # 启动连接处理线程
            threading.Thread(target=self._handle_connections, daemon=True).start()

            # 自动打开浏览器
            webbrowser.open(f"http://localhost:{self.local_port}")

            return True

        except Exception as e:
            print(f"启动隧道失败: {str(e)}")
            self.stop()
            return False

    def _handle_connections(self) -> None:
        """处理本地的连接请求"""
        while self.running:
            try:
                # 接受本地的连接
                local_socket, addr = self.listener.accept()
                print(f"新的连接: {addr}")

                # 建立到远程的通道
                remote_channel = self.transport.open_channel(
                    'direct-tcpip',
                    (self.target_host, self.target_port),
                    ('localhost', self.local_port)
                )

                # 启动双向数据转发
                threading.Thread(
                    target=self._forward_data,
                    args=(local_socket, remote_channel, "本地到远程"),
                    daemon=True
                ).start()
                threading.Thread(
                    target=self._forward_data,
                    args=(remote_channel, local_socket, "远程到本地"),
                    daemon=True
                ).start()

            except Exception as e:
                if self.running:
                    print(f"处理连接错误: {str(e)}")

    def _forward_data(self, source, destination, direction: str) -> None:
        """在两个端点之间转发数据"""
        try:
            while self.running:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except Exception as e:
            if self.running:
                print(f"{direction} 数据转发错误: {str(e)}")
        finally:
            source.close()
            destination.close()
            print(f"{direction} 连接已关闭")

    def stop(self) -> None:
        """停止隧道并清理资源"""
        self.running = False
        if self.listener:
            try:
                self.listener.close()
            except:
                pass
        if self.ssh_client:
            try:
                self.ssh_client.close()
            except:
                pass
        print("SSH隧道已关闭")


if __name__ == "__main__":
    # 配置参数
    config = {
        "ssh_host": "",
        "ssh_port": 22,
        "ssh_user": "root",
        "ssh_password": "",
        # "ssh_key": "/path/to/private/key",  # 或使用 ssh_key
        "local_port": 8080,
        "target_host": "",  # 目标服务器
        "target_port": 80  # 目标服务器端口
    }

    # 创建并启动隧道
    tunnel = WebSSHTunnel(**config)
    if tunnel.start():
        try:
            # 保持隧道运行
            while True:
                time.sleep(3600)  # 每小时检查一次
        except KeyboardInterrupt:
            print("\n用户中断，关闭隧道...")
            tunnel.stop()
```
