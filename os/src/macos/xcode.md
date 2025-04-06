# Xcode

## 安装 Xcode

1. [https://developer.apple.com/download/all/](https://developer.apple.com/download/all/)
2. 登录苹果账号
3. 下载 [Xcode 16.2.xip](https://download.developer.apple.com/Developer_Tools/Xcode_16.2/Xcode_16.2.xip)
4. 解压得到 Xcode.app

### licence

新安装的 Xcode 需要签收同意它的 licence。其方式比较独特，即在命令行中输入

```sh
sudo xcodebuild -license
```

然后会弹出很多文本内容，即 licence 内容。不用看直接不停按 tab 键滑到文件最后，然后输入一个 agree，敲回车即可。如果这里不同意 licence 后续使用 xcode 的时候会报错。

## 安装 Command Line Tools (CLT) for Xcode

1. [https://developer.apple.com/download/all/](https://developer.apple.com/download/all/)
2. 登录苹果账号
3. 下载 [Command_Line_Tools_for_Xcode_16.2](https://download.developer.apple.com/Developer_Tools/Command_Line_Tools_for_Xcode_16.2/Command_Line_Tools_for_Xcode_16.2.dmg)
4. 安装
