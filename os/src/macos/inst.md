# 安装软件

## app store

```
QuickRec-Screen Recording
bob
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

## 安装其它软件

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
```

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
