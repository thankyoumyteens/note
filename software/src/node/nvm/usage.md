# Node.js 版本管理 (查看、安装与卸载)

### 查看 Node.js 版本

```sh
# 列出所有可下载的远程 Node.js 版本
nvm ls-remote

# 列出本地已安装的所有 Node.js 版本
nvm ls
```

### 安装 Node.js 版本

```sh
# 安装指定的具体版本
nvm install 16.15.1

# 安装最新的 LTS (长期支持) 版本（推荐）
nvm install --lts

# 安装最新版 (Current)
nvm install node
```

### 卸载 Node.js 版本

```sh
# 卸载指定的本地版本
nvm uninstall 16.15.1
```
