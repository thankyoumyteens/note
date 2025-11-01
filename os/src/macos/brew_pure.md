# Homebrew

## 安装

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 设置环境变量
echo >> /Users/walter/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/walter/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# 验证
brew help
```

## 卸载

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
```
