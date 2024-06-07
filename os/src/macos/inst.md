# 安装软件

## 初始化 git

git 在安装 Command Line Tools (CLT) for Xcode 时自带:

```sh
git config --global user.name "zhaosz"
git config --global user.email "iloveyesterday@outlook.com"
ssh-keygen -t rsa -C "iloveyesterday@outlook.com"
# 设置为区分大小写
git config --global core.ignorecase false
```

## 安装 jdk

1. 下载:

   - [Liberica](https://bell-sw.com/pages/downloads/)
   - [Adoptium](https://adoptium.net/zh-CN/temurin/releases/)
   - [Zulu](https://www.azul.com/downloads/?package=jdk#zulu)
   - [Microsoft](https://learn.microsoft.com/zh-cn/java/openjdk/download)

2. 配置环境变量:

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export JAVA_HOME=/Users/walter/walter/jdk/jdk-21.0.2.jdk
export PATH=$JAVA_HOME/bin:$PATH

# 使环境变量生效
source ~/.zshrc
```

3. 验证:

```sh
java -version
```

4. 报错: 无法打开"java", 因为无法验证开发者:

   1. 左上角 apple -> 系统设置 -> 隐私与安全性 -> 安全性
   2. 已阻止使用"java", 因为来自身分不明的开发者
   3. 仍要打开

## 安装 python

```sh
brew install python3
brew install python-tk

pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 config set global.trusted-host pypi.tuna.tsinghua.edu.cn
pip3 config set global.timeout 120
```

## 安装 jd-gui

1. 下载并解压: [jd-gui-osx-1.6.6.tar](https://github.com/java-decompiler/jd-gui/releases/download/v1.6.6/jd-gui-osx-1.6.6.tar)

2. JD-GUI.app 上右键 -> 显示包内容

3. 编辑 `JD-GUI.app/Contents/MacOS/universalJavaApplicationStub.sh` 文件:

```sh
# 把这里:
# else
	# JAVACMD="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
# fi
# 替换成下面:
else
	JAVACMD="必须是JDK8的路径/bin/java"
fi
```

## 安装 7-zip

1. 下载: [7z2301-mac.tar.xz](https://www.7-zip.org/a/7z2301-mac.tar.xz)

2. 解压:

```sh
mkdir 7z2301
tar -xvf 7z2301-mac.tar.xz -C 7z2301/
```

3. 配置环境变量:

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export PATH=/Users/walter/walter/software/7z2301:$PATH

# 使环境变量生效
source ~/.zshrc

```

4. 验证

```sh
7zz -h
```

## 安装 nvm

1. 安装:

```sh
brew install nvm
```

2. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

# 使环境变量生效
source ~/.zshrc
```

3. 验证

```sh
nvm help
```

## 安装 node.js

```sh
nvm install 16.15.1
```

切换 node 版本:

```sh
# nvm use 只能在当前控制台临时修改版本
nvm use 16.15.1
# 全局设置默认 node 版本
nvm alias default 16.15.1
```

配置国内源:

```sh
npm config set registry https://registry.npmmirror.com
```

## 安装 redis

1. 下载解压源码:

```sh
wget https://mirrors.huaweicloud.com/redis/redis-7.2.4.tar.gz
tar -zxvf redis-7.2.4.tar.gz
```

2. 修改 `src/Makefile` 文件:

```sh
# 改成安装路径
PREFIX?=/Users/walter/walter/software/redis
INSTALL_BIN=$(PREFIX)
```

3. 安装:

```sh
make
make install
```

4. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export PATH=/Users/walter/walter/software/redis:$PATH

# 使环境变量生效
source ~/.zshrc
```

## 安装其它软件

```sh
# chrome
brew install --cask google-chrome
# subversion
brew install subversion
# vlc
brew install vlc
# 鼠标滚轮
brew install mos
# mdbook
brew install mdbook
# ffmpeg
brew install ffmpeg
# wget
brew install wget
```

- [Jetbrains IntelliJ IDEA](https://www.jetbrains.com/idea/download/other.html)
- [Jetbrains CLion](https://www.jetbrains.com/clion/download/other.html)
- [Jetbrains PyCharm](https://www.jetbrains.com/pycharm/download/other.html)
- [Jetbrains WebStorm](https://www.jetbrains.com/webstorm/download/other.html)
- [Android Studio](https://developer.android.google.cn/studio?hl=zh-cn)
- [vscodium](https://github.com/VSCodium/vscodium/releases)
- [flutter](https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra/releases/stable/macos/)
- [gradle](https://mirrors.cloud.tencent.com/gradle/)
- [maven](https://repo.huaweicloud.com/apache/maven/maven-3/)
- [AnotherRedisDesktopManager](https://gitee.com/qishibo/AnotherRedisDesktopManager/releases)
- [dbeaver](https://github.com/dbeaver/dbeaver/releases)
- [tabby](https://github.com/Eugeny/tabby/releases)
- [parallels desktop](https://www.parallels.cn/products/desktop/download/) 虚拟机
- [UTM](https://github.com/utmapp/UTM/releases) 虚拟机
- [Snipaste](https://zh.snipaste.com/download.html) 截图
- [obs](https://github.com/obsproject/obs-studio/releases) 录屏
- [downkyicore](https://github.com/yaobiao131/downkyicore/releases)
- [drawio](https://github.com/jgraph/drawio-desktop/releases)
- [Motrix](https://github.com/agalwood/Motrix/releases)
- [Whisky](https://github.com/Whisky-App/Whisky/releases) wine
- [upscayl](https://github.com/upscayl/upscayl/releases) 图片放大
- [tinyImage](https://github.com/focusbe/tinyImage/releases) 图片压缩
- [mactex](https://www.tug.org/mactex/mactex-download.html) latex
- [texstudio](https://github.com/texstudio-org/texstudio/releases) latex 编辑器
- [GIMP](https://www.gimp.org/downloads/) 修图
- [kdenlive](https://kdenlive.org/zh/download-zh/) 剪视频
- [calibre](https://github.com/kovidgoyal/calibre/releases)
