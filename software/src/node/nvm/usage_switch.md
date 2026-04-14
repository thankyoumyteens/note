# 切换 Node.js 版本

```sh
# 临时切换（仅在当前终端窗口有效）
nvm use 16.15.1

# 切换到最新的 LTS 版本
nvm use --lts

# 全局设置默认 Node 版本（新开终端窗口时默认使用的版本）
nvm alias default 16.15.1
```

### 验证当前正在使用的版本

```sh
node -v
npm -v
```
