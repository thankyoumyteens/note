# 安装nvm

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
```

# 重启终端

```sh
nvm --version
```

# 安装node

高版本的nodejs需要更高版本的glibc编译环境, 而升级glibc可能会对系统稳定性产生影响, 所以建议降低node.js的版本, 去兼容低版本glibc。

```sh
nvm install 16.15.1
```

# 切换node版本

```sh
nvm use 16.15.1
```

# 配置国内源

```sh
npm config set registry https://registry.npmmirror.com
```
