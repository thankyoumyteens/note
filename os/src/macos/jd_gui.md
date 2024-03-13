# 安装 jd-gui

下载: [jd-gui-osx-1.6.6.tar](https://github.com/java-decompiler/jd-gui/releases/download/v1.6.6/jd-gui-osx-1.6.6.tar)

解压

JD-GUI.app 上右键 -> 显示包内容

编辑 JD-GUI.app/Contents/MacOS/universalJavaApplicationStub.sh 文件:

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
