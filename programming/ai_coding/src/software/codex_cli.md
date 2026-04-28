# 安装 Codex CLI

在 macOS 环境下，最便捷的方式是直接使用 Homebrew 进行安装；如果你习惯使用 Node 工具链，也可以使用 npm。

**方法 1：使用 Homebrew**

```bash
brew install codex
```

**方法 2：使用 npm（需要 Node.js 环境）**

```bash
npm install -g @openai/codex
```

---

## 配置代理

```sh
vim ~/.zshrc

# 追加到文件末尾
alias codex_proxy="http_proxy=http://127.0.0.1:10808 https_proxy=http://127.0.0.1:10808 all_proxy=socks5://127.0.0.1:10808 codex"

# 使配置生效
source ~/.zshrc

# 启动 codex（带着代理）
codex_proxy
```
