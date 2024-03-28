# Win11 编译 OpenJDK21

## 下载 openjdk 源码

[jdk-21-ga](https://github.com/openjdk/jdk21/archive/refs/tags/jdk-21-ga.zip)

## 下载 bootstrap-jdk

[Liberica JDK](https://download.bell-sw.com/java/21.0.1+12/bellsoft-jdk21.0.1+12-windows-amd64.zip)

## 下载 cygwin

[cygwin](https://www.cygwin.com/setup-x86_64.exe)

由于默认的安装只会安装一些必要的软件, 所以安装过程中需要选择安装一些额外的包:

- binutils
- make
- m4
- cpio
- zip
- unzip
- procps-ng
- autoconf

## 下载 Visual Studio 2022

[VS2022](https://c2rsetup.officeapps.live.com/c2r/downloadVS.aspx?sku=community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030:46b60c8c2da84e9cb9b6d5a777cf449e)

管理员打开 cmd:

```sh
fsutil file setshortname "C:\Program Files (x86)\Windows Kits" Kits
```

## 编译

打开 cygwin, 输入命令:

```sh
cd /cygdrive/c/Users/Public/jdk21-jdk-21-ga

bash configure --with-debug-level=slowdebug --with-native-debug-symbols=external --disable-warnings-as-errors --with-boot-jdk=/cygdrive/c/Users/Public/jdk-21.0.1 --with-tools-dir="/cygdrive/c/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build"

make images CONF=windows-x86_64-server-slowdebug

./build/\*/images/jdk/bin/java -version

make compile-commands
```

## 编译报错

报错: Target CPU mismatch. We are building for x86_64 but CL is for ""; expected "x64"

打开 make/autoconf/toolchain.m4

找到相应的字串 Target CPU mismatch, 有两个办法:

1. 注释这一段 if
2. 把 AC_MSG_ERROR 改成 AC_MSG_RESULT
