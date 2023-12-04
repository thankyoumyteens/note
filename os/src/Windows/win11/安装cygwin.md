# 安装 cygwin

[setup-x86_64.exe](https://www.cygwin.com/setup-x86_64.exe)

由于默认的安装只会安装一些必要的软件, 所以安装过程中需要选择安装一些额外的包:

- wget

## 安装包管理器

```sh
wget -c https://raw.githubusercontent.com/transcode-open/apt-cyg/master/apt-cyg
install apt-cyg /bin
apt-cyg mirror https://mirrors.huaweicloud.com/cygwin/
apt-cyg update
```

## 安装软件

```sh
apt-cyg install vim
apt-cyg install chere
```

## 添加到右键菜单

使用管理员身份运行 cygwin:

```sh
chere -i -t mintty -s bash
```

此时右键菜单应该有 Bash Prompt Here 菜单选项。

更改注册表:

```sh
计算机\HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\background\shell\cygwin64_bash
```

增加 Icon 字符串, 值设置为: C:\cygwin64\Cygwin.ico。
