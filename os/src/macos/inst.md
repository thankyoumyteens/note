# 安装软件

## app store

```
QuickRec-Screen Recording
bob
```

## git

git 在安装 Command Line Tools (CLT) for Xcode 时自带:

```sh
git config --global user.name "zhaosz"
git config --global user.email "iloveyesterday@outlook.com"
ssh-keygen -t rsa -C "iloveyesterday@outlook.com"
# 设置为区分大小写
git config --global core.ignorecase false
```

## jdk

下载:

- [Liberica](https://bell-sw.com/pages/downloads/)
- [Adoptium](https://mirrors.tuna.tsinghua.edu.cn/Adoptium)
- [Zulu](https://www.azul.com/downloads/?package=jdk#zulu)
- [Microsoft](https://learn.microsoft.com/zh-cn/java/openjdk/download)

配置:

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export JAVA_HOME=/Users/walter/walter/jdk/jdk-21.0.2.jdk
export PATH=$JAVA_HOME/bin:$PATH

# 使环境变量生效
source ~/.zshrc

# 验证
java -version
```

### 报错: 无法打开"java", 因为无法验证开发者:

1.  左上角 apple -> 系统设置 -> 隐私与安全性 -> 安全性
2.  已阻止使用"java", 因为来自身分不明的开发者
3.  仍要打开

## python

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

## 使用 Homebrew 安装的软件

```sh
# chrome
brew install --cask google-chrome
# svn
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
# ip命令
brew install iproute2mac
# 将PlantUML脚本转换成图片
brew install graphviz
# PlantUML
brew install plantuml
```

## 其它软件

- [Anaconda](https://www.anaconda.com/download/success)
- [Android Studio](https://developer.android.google.cn/studio?hl=zh-cn)
- [AnotherRedisDesktopManager](https://gitee.com/qishibo/AnotherRedisDesktopManager/releases)
- [calibre](https://github.com/kovidgoyal/calibre/releases)
- [dbeaver](https://github.com/dbeaver/dbeaver/releases)
- [downkyicore](https://github.com/yaobiao131/downkyicore/releases)
- [drawio](https://github.com/jgraph/drawio-desktop/releases)
- [flutter](https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra/releases/stable/macos/)
- [GIMP](https://www.gimp.org/downloads/) 修图
- [gradle](https://mirrors.cloud.tencent.com/gradle/)
- [HandBrake](https://github.com/HandBrake/HandBrake/releases) 视频格式转换
- [LiveRecorder](https://github.com/auqhjjqdo/LiveRecorder) 无人值守直播录制脚本
- [localsend](https://github.com/localsend/localsend)
- [录播姬](https://rec.danmuji.org/install/desktop/) 录 B 站直播
- [Jetbrains CLion](https://www.jetbrains.com/clion/download/other.html)
- [Jetbrains GoLand](https://www.jetbrains.com/go/download/other.html)
- [Jetbrains IntelliJ IDEA](https://www.jetbrains.com/idea/download/other.html)
- [Jetbrains PyCharm](https://www.jetbrains.com/pycharm/download/other.html)
- [Jetbrains WebStorm](https://www.jetbrains.com/webstorm/download/other.html)
- [kdenlive](https://kdenlive.org/zh/download-zh/) 剪视频
- [mactex](https://www.tug.org/mactex/mactex-download.html) latex
- [maven](https://repo.huaweicloud.com/apache/maven/maven-3/)
- [Motrix](https://github.com/agalwood/Motrix/releases)
- [Snipaste](https://zh.snipaste.com/download.html) 截图
- [tabby](https://github.com/Eugeny/tabby/releases)
- [texstudio](https://github.com/texstudio-org/texstudio/releases) latex 编辑器
- [tinyImage](https://github.com/focusbe/tinyImage/releases) 图片压缩
- [upscayl](https://github.com/upscayl/upscayl/releases) 图片放大
- [UTM](https://github.com/utmapp/UTM/releases) 虚拟机
- [vscodium](https://github.com/VSCodium/vscodium/releases)
- [Whisky](https://github.com/Whisky-App/Whisky/releases) wine
