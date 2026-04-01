# 安装Poetry

### 1. 安装

官方推荐的做法是将其安装在全局独立环境中（避免与项目依赖冲突）。你可以使用以下命令安装：

Windows (PowerShell):

```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

macOS / Linux:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export PATH="/Users/walter/.local/bin:$PATH"

# 使环境变量生效
source ~/.zshrc

# 验证
poetry --version
```
