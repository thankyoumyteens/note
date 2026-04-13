# 安装 Gemini CLI

### 1. 安装

```sh
npm install -g @google/gemini-cli
```

### 2. 配置代理

```sh
vim ~/.zshrc

# 追加到文件末尾
alias gemini_proxy="http_proxy=http://127.0.0.1:10808 https_proxy=http://127.0.0.1:10808 all_proxy=socks5://127.0.0.1:10808 gemini"

# 使配置生效
source ~/.zshrc
```

### 3. 启动 gemini（带着代理）

```sh
gemini_proxy
```
