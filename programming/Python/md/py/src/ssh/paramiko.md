# 安装

```
pip install paramiko
```

# SSHClient

## 密码连接方式

```py
import paramiko   
# 实例化SSHClient  
ssh_client = paramiko.SSHClient()   
# 自动添加策略, 保存服务器的主机名和密钥信息, 如果不添加, 那么不再本地know_hosts文件中记录的主机将无法连接 , 此方法必须放在connect方法的前面
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
# 连接SSH服务端, 以用户名和密码进行认证 , 调用connect方法连接服务器
ssh_client.connect(hostname='192.168.137.105', port=22, username='root', password='123456')   
# 打开一个Channel并执行命令  结果放到stdout中, 如果有错误将放到stderr中
stdin, stdout, stderr = ssh_client.exec_command('df -hT ') 
# stdout 为正确输出, stderr为错误输出, 同时是有1个变量有值   
# 打印执行结果 
print(stdout.read().decode('utf-8'))  
# 关闭SSHClient连接 
ssh_client.close()
```

## 密钥连接方式

```py
# 配置私人密钥文件位置
private = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa') 
#实例化SSHClient
ssh_client = paramiko.SSHClient() 
#自动添加策略, 保存服务器的主机名和密钥信息, 如果不添加, 那么不再本地know_hosts文件中记录的主机将无法连接
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
#连接SSH服务端, 以用户名和密钥进行认证
ssh_client.connect(hostname='192.168.137.100', port=22, username='root', pkey=private)
```

## connect()

实现远程服务器的连接与认证, 对于该方法只有hostname是必传参数

- hostname 连接的目标主机
- port=SSH_PORT 指定端口
- username=None 验证的用户名
- password=None 验证的用户密码
- pkey=None 私钥方式用于身份验证
- key_filename=None 一个文件名或文件列表, 指定私钥文件
- timeout=None 可选的tcp连接超时时间
- allow_agent=True, 是否允许连接到ssh代理, 默认为True 允许
- look_for_keys=True 是否在~/.ssh中搜索私钥文件, 默认为True 允许
- compress=False, 是否打开压缩

## set_missing_host_key_policy()

设置连接的远程主机没有本地主机密钥或HostKeys对象时的策略

- AutoAddPolicy 自动添加主机名及主机密钥到本地HostKeys对象, 不依赖load_system_host_key的配置。即新建立ssh连接时不需要再输入yes或no进行确认
- WarningPolicy 用于记录一个未知的主机密钥的python警告。并接受, 功能上和AutoAddPolicy类似, 但是会提示是新连接
- RejectPolicy 自动拒绝未知的主机名和密钥, 依赖load_system_host_key的配置。此为默认选项

## exec_command()

在远程服务器执行Linux命令

```py
# 使用exec_command执行多条命令
# 加上get_pty=True参数, 多条命令用分号隔开
std_in,std_out,std_err = ssh_client.exec_command('cd /home;tar -zxvf requests-2.13.0.tar.gz;cd requests-2.13.0;sudo -S python setup.py install',get_pty=True)
# 执行输入命令, 输入sudo命令的密码, 会自动执行
std_in.write('PWD'+'\n')
for line in std_out:
    print line.strip('\n')
```

## invoke_shell()

开启一个shell终端

```py
shell = ssh_client.invoke_shell()
for cmd in cmds:
    # 执行命令
    shell.send(cmd + '\n')
    output_bytes = self.get_recv_data(shell)
    print(output_bytes.decode())
    while True:
        # 等待shell输出
        if not shell.recv_ready():
            time.sleep(0.5)
        else:
        return None
    # 接收输出结果
    output_bytes = bytes()
    o = shell.recv(1024)
    output_bytes += o
    while shell.recv_ready():
        o = shell.recv(1024)
        output_bytes += o
    print(output_bytes.decode())
shell.close()
```

- send(string) 向shell发送命令
- recv(nbytes) 接收shell返回的数据, nbytes: 最大读取的字节数
- recv_ready() 可以读取shell中数据时返回True

## open_sftp()

在当前ssh会话的基础上创建一个sftp会话。该方法会返回一个SFTPClient对象

```py
# 利用SSHClient对象的open_sftp()方法, 可以直接返回一个基于当前连接的sftp对象, 可以进行文件的上传等操作. 
sftp = ssh_client.open_sftp()
sftp.put('local.txt','remote.txt')
```

# SFTPClient

- put(localpath, remotepath, callback=None, confirm=True) 将本地文件上传到服务器, confirm: 是否调用stat()方法检查文件状态, 返回ls -l的结果
- get(remotepath, localpath, callback=None) 从服务器下载文件到本地
- mkdir() 在服务器上创建目录
- remove() 在服务器上删除目录
- rename() 在服务器上重命名目录
- stat() 查看服务器文件状态
- listdir() 列出服务器目录下的文件

```py
import paramiko 
# 实例化一个transport对象
tran = paramiko.Transport(('192.168.137.100', 22)) 
# 连接SSH服务端, 使用password
tran.connect(username="root", password='123456')
# 或使用密钥连接
#private = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
# tran.connect(username="root", pkey=private) 
# 获取SFTP实例
sftp = paramiko.SFTPClient.from_transport(tran) 
# 设置上传的本地/远程文件路径
local_path = "/home/1.txt"
remote_path = "/tmp/1.txt" 
# 执行上传动作
sftp.put(local_path, remote_path)
# 执行下载动作
sftp.get(remote_path, local_path) 
# 关闭Transport通道
tran.close()
```
