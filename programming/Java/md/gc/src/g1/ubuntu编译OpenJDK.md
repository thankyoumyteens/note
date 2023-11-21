# ubuntu 编译 OpenJDK

## 下载 VirtualBox

[VirtualBox-7.0.12-159484-Win.exe](https://download.virtualbox.org/virtualbox/7.0.12/VirtualBox-7.0.12-159484-Win.exe)

## 下载 Ubuntu14.04.6

[ubuntu-14.04.6-desktop-amd64.iso](https://releases.ubuntu.com/14.04/ubuntu-14.04.6-desktop-amd64.iso)

## 下载 jdk8-b120

[jdk8-b120.tar.gz](https://github.com/openjdk/jdk/archive/refs/tags/jdk8-b120.tar.gz)

## 新建虚拟机

- 新建 -> 虚拟光盘选择 ubuntu-14.04.6-desktop-amd64.iso
- 进入 ubuntu 系统
- 设备 -> 安装增强功能
- 安装完成后重启

## 设置共享文件夹

- 设备 -> 共享粘贴板 -> 双向
- 设备 -> 共享文件夹 -> 共享文件夹... -> 选择共享文件夹路径(把源码所在的文件夹作为共享文件夹), 自动挂载, 固定分配 -> 确定
- 打开终端

### 添加 sudo 权限

```sh
su
apt install -y vim
vim /etc/sudoers
```

添加一行：

```
用户名  ALL=(ALL:ALL)  ALL
```

保存：

```sh
wq!
```

退出 su：

```sh
exit
```

### 添加共享文件夹访问权限

```sh
sudo usermod -aG vboxsf $(whoami)
```

重启后验证：

```sh
ll /media/sf_others/
```

## 把源码复制到虚拟机内部

```sh
cp /media/sf_others/jdk-jdk8-b120.tar.gz ~/jdk-jdk8-b120.tar.gz
tar -zxvf jdk-jdk8-b120.tar.gz
cd jdk-jdk8-b120
```

## 编译

```sh
sudo apt-get install -y openjdk-7-jdk
sudo apt-get install -y libX11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev
sudo apt-get install -y libcups2-dev
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y libasound2-dev
sudo chmod 777 configure
./configure --with-target-bits=64 --with-debug-level=slowdebug
make
```

## 报错：This os not support

查看 os 版本：

```sh
uname -r
```

修改 makefile：

```sh
vim hotspot/make/linux/Makefile
```

修改：

```conf
# 修改前的内容
# SUPPORTED_OS_VERSION = 2.4% 2.5% 2.6% 3%
# 如果uname -r返回4.4.0-142-generic，则添加4%
SUPPORTED_OS_VERSION = 2.4% 2.5% 2.6% 3% 4%
```

保存，重新执行 make

## 验证

```sh
build/linux-x86_64-normal-server-slowdebug/jdk/bin/java -version
```
