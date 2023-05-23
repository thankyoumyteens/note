# Linux

官网: [nvm-sh](https://github.com/nvm-sh/nvm)

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```
或
```
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```
安装完要重新打开Terminal来重启会话

# Windows

[https://github.com/coreybutler/nvm-windows/releases](https://github.com/coreybutler/nvm-windows/releases)

# 设置镜像

在nvm的安装目录，修改settings.txt

```
nvm npm_mirror https://npmmirror.com/mirrors/npm/
nvm node_mirror https://npmmirror.com/mirrors/node/
```

# 查看当前电脑上的node版本

```
nvm list
```

# 安装nodejs不同版本

```
nvm install 16.8.0
```

# 切换node版本

```
nvm use 16.8.0
```

# 卸载

```
nvm uninstall 16.8.0
```
