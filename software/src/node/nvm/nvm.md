# nvm (Node Version Manager) 安装与使用指南

`nvm` 是一个用于管理多个活跃 Node.js 版本的命令行工具。它允许你在同一台机器上轻松安装、切换和管理不同版本的 Node.js，非常适合处理需要不同 Node.js 环境的多个项目。

## 1. 安装 (基于 macOS Homebrew)

在终端中运行以下命令安装 nvm：

```sh
brew install nvm
```

## 2. 配置环境变量

安装完成后，需要将 nvm 加载到你的 shell 中。

```sh
# 1. 创建 nvm 工作目录
mkdir ~/.nvm

# 2. 打开 zsh 配置文件（如果你使用的是 bash，请修改 ~/.bash_profile）
vim ~/.zshrc

# 3. 在 ~/.zshrc 文件末尾添加以下内容：
export NVM_DIR="$HOME/.nvm"
# 注意：以下路径为 Apple Silicon (M1/M2/M3) 的 Homebrew 默认路径。
# 如果你是 Intel 芯片的 Mac，请将 /opt/homebrew/ 替换为 /usr/local/
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion
```

保存并退出 vim (`:wq`) 后，使环境变量立即生效：

```sh
source ~/.zshrc
```

## 3. 验证安装

检查 nvm 是否安装成功并输出版本号：

```sh
nvm -v
# 或者查看帮助文档
nvm help
```

## npm 国内配置

为了提升国内下载依赖的速度，建议将 npm 的源切换为国内镜像源（如淘宝/阿里云镜像）：

```sh
# 配置 npm 国内镜像源
npm config set registry https://registry.npmmirror.com

# 验证配置是否成功
npm config get registry

# 还原官方默认源
npm config delete registry
```
