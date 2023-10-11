# 安装 lrzsz

```
yum install lrzsz -y
```

# rz命令

rz命令（Receive ZMODEM），使用ZMODEM协议，将本地文件批量上传到远程Linux/Unix服务器，注意不能上传文件夹。

当我们使用虚拟终端软件，如Xshell、SecureCRT或PuTTY来连接远程服务器后，使用rz命令可以上传本地文件到远程服务器。输入rz回车后，会出现文件选择对话框，选择需要上传文件，一次可以指定多个文件，上传到服务器的路径为当前执行rz命令的目录。

此外，可以在虚拟终端软件设置上传时默认加载的本地路径和下载的路径。

```
rz [选项]
```

## 选项

- `-+, --append`:将文件内容追加到已存在的同名文件
- `-a,--ascii`:以文本方式传输
- `-b, --binary`:以二进制方式传输，推荐使用
- `--delay-startup N`:等待N秒
- `-e, --escape`:对所有控制字符转义，建议使用
- `-E, --rename`:已存在同名文件则重命名新上传的文件，以点和数字作为后缀
- `-p, --protect`:对ZMODEM协议有效，如果目标文件已存在则跳过 -
- `q, --quiet`:安静执行，不输出提示信息
- `-v, --verbose`:输出传输过程中的提示信息
- `-y, --overwrite`:存在同名文件则替换
- `-X, --xmodem`:使用XMODEM协议
- `--ymodem`:使用YMODEM协议
- `-Z, --zmodem`:使用ZMODEM协议
- `--version`：显示版本信息
- `--h, --help`：显示帮助信息

# sz命令

sz命令（Send ZMODEM）通过ZMODEM协议，可将多个文件从远程服务器下载到本地。注意不能下载文件夹，如果下载文件夹，请先打包再下载

```
rz [选项] [filelist]
```

## 选项

选项基本与rz相同
