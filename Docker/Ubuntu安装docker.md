# Ubuntu 18.04 安装docker ce

## 卸载老版本

如果你安装了老版本, 请卸载掉
```
$ sudo apt-get remove docker docker-engine docker.io
```

## 设置存储库

更新apt包索引
```
$ sudo apt-get update
```
安装包以允许通过HTTPS使用存储库：
```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```
添加Docker的官方GPG密钥：
```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
通过搜索指纹的最后8个字符, 确认您现在拥有指纹9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88的密钥。
```
$ sudo apt-key fingerprint 0EBFCD88

pub   4096R/0EBFCD88 2017-02-22
      Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid                  Docker Release (CE deb) <docker@docker.com>
sub   4096R/F273FCD8 2017-02-22
```
使用以下命令设置稳定存储库。
* 注意：`lsb_release -cs`子命令返回Ubuntu发行版的名称, 例如xenial
```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
## 安装DOCKER CE

更新apt包索引。
```
sudo apt-get update
```
安装最新版本的Docker CE, 或转到下一步安装特定版本：
```
$ sudo apt-get install docker-ce
```
查看Docker CE 版本
```
docker -v 
Docker version 18.06.1-ce, build e68fc7a
```
通过运行hello-world映像验证是否正确安装了Docker CE。
```
$ sudo docker run hello-world
```
出现下面这个表示你安装成功：
```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```
