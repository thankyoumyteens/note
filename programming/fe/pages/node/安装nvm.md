# Linux

官网: [nvm-sh](https://github.com/nvm-sh/nvm)

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```
或
```
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```
安装完要重新打开Terminal来重启会话

# Windows

[https://github.com/coreybutler/nvm-windows/releases](https://github.com/coreybutler/nvm-windows/releases)

# 使用

安装最新版 Node.js
```
nvm install node
```

安装 LTS 版
```
nvm install --lts
```

安装指定版本
```
nvm install 14
```

使用最新版本
```
nvm use node
```

使用指定版本
```
nvm use 14
```

设置别名
```
nvm alias 6 v6.9.5
```
