# 安装 pot

- [pot](https://github.com/pot-app/pot-desktop)

## 由于开发者无法验证, “pot”无法打开。

点击 取消 按钮, 然后去 设置 -> 隐私与安全性 页面, 点击 仍要打开 按钮, 然后在弹出窗口里点击 打开 按钮即可, 以后打开 pot 就再也不会有任何弹窗告警了

## 启动时提示文件损坏

打开 Terminal.app, 并输入以下命令, 然后重启 pot 即可: 

```sh
sudo xattr -d com.apple.quarantine /Applications/pot.app
```

## 每次打开时都遇到辅助功能权限提示

如果每次打开时都遇到辅助功能权限提示, 或者无法进行划词翻译, 请前往设置 -> 隐私与安全 -> 辅助功能, 移除 “pot”, 并重新添加 “pot”。
