# Codex CLI 配置 spec-workflow-mcp

编辑 Codex 全局配置文件：

```bash
vim ~/.codex/config.toml
```

加入：

```toml
[mcp_servers.spec-workflow]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "/path/to/your/project"
]
```

然后重启 Codex CLI。

## 支持多项目

不要在全局配置文件(`~/.codex/config.toml`)中配置。而是在每个项目的根目录下创建 codex 配置文件:

```sh
mkdir .codex
vim .codex/config.toml
```

添加下面内容:

```toml
[mcp_servers.spec-workflow]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "/path/to/your/project"
]
```
