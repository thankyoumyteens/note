# nvm

1. 安装:

```sh
brew install nvm
```

2. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

# 使环境变量生效
source ~/.zshrc
```

3. 验证

```sh
nvm help
```

## 安装 node.js

```sh
nvm install 16.15.1
```

切换 node 版本:

```sh
# nvm use 只能在当前控制台临时修改版本
nvm use 16.15.1
# 全局设置默认 node 版本
nvm alias default 16.15.1
```

配置国内源:

```sh
npm config set registry https://registry.npmmirror.com
```
