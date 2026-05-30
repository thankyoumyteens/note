# 前置环境

先确认你本地有 Node.js 和 npx：

```bash
node -v
npx -v
```

如果没有，建议用 Homebrew 安装：

```bash
brew install node
```

然后重新检查：

```bash
node -v
npx -v
```

不需要全局安装 `spec-workflow-mcp`，优先用：

```bash
npx -y @pimzino/spec-workflow-mcp@latest
```

这样每次取最新包，避免全局版本污染。

如果你是用 npm install -g 全局安装的，直接卸载：

```sh
npm uninstall -g @pimzino/spec-workflow-mcp
```

然后检查是否还存在：

```sh
npm list -g --depth=0 | grep spec-workflow
```
