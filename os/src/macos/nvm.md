# 安装 nodejs

## 安装 nvm

```sh
brew install nvm
```

## 配置环境变量

1. 打开配置文件

```sh
vim ~/.zshrc
```

2. 在最后一行添加:

```conf
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion
```

3. 使环境变量生效

```sh
source ~/.zshrc
```

## 验证

```sh
nvm help
```

## 安装 node

```sh
nvm install 16.15.1
```

## 切换 node 版本

```sh
nvm use 16.15.1
```

## 配置国内源

```sh
npm config set registry https://registry.npmmirror.com
```
