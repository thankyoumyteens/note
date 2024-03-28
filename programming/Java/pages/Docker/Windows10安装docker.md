# 开启安装windows10的WSL2功能

要升级 windows10 专业版系统到 win10 v2004 的内部版本 19041 或更高版本

在"控制面板\所有控制面板项\程序和功能"中选择"启用或者关闭Windows功能", 勾选:
- 适用于Linux的Windows子系统
- 虚拟机平台

在 https://docs.microsoft.com/zh-cn/windows/wsl/wsl2-kernel 页面点击下载 linux 内核更新包, 下载完点击安装

重启系统并设置WSL 2 设置为默认版本
```
wsl --set-default-version 2
```
查看是不是WSL2, 
```
wsl -l -v
```

# 安装 Ubuntu

打开 Microsoft Store, 搜索 Terminal, 安装 Windows Terminal, 用于后面和 WSL 子系统交互。

搜索 Ubuntu, 选择安装。

如果 Microsoft Store 应用不可用, 则可以通过单击以下链接来下载并手动安装 Linux 发行版: https://aka.ms/wsl-ubuntu-1604
安装Linux
```
Add-AppxPackage .\app_name.appx
```

安装完成后, 第一次打开 Ubuntu 的时候, 将打开一个控制台窗口, 会等待几分钟来进行配置, 启动完成后为 Ubuntu 创建一个用户和密码(如果第一次启动ubuntu失败, 可以重启windows10系统再次试下)。

为了避免sudo切换root是需要输入密码, 把自己配置的用户名加到sudo免密中, 命令如下: 
```
sudo echo "用户名 ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers 
```

# 更换ubuntu的apt安装源

备份配置文件
```
sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
```
修改sources.list文件
```
sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
```
更新索引
```
sudo apt-get update
sudo apt-get upgrade -y
```

# 安装docker

下载最新的 Docker Desktop for Windows 程序 , 建议下载stable版本。下载地址: https://www.docker.com/products/docker-desktop

启动Docker Desktop for Windows, 点击"设置"按钮, 启用基于WSL2的引擎复选框(Use the WSL 2 based engine)

在 Resources 的WSL Integration中设置要从哪个 WSL2 发行版中访问 Docker, morendocker会新建wsl用于安装。
