# 配置到 Codex

编辑 Codex 配置文件：

```bash
code ~/.codex/config.toml
```

没有 VS Code 的话用：

```bash
nano ~/.codex/config.toml
```

加入：

```toml
[mcp_servers.spec-workflow]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "/path/to/ai-doc-summary"
]
startup_timeout_sec = 20
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
  "/path/to/ai-doc-summary"
]
startup_timeout_sec = 20

[mcp_servers.spec-workflow.tools.approvals]
approval_mode = "approve"

[mcp_servers.spec-workflow.tools.log-implementation]
approval_mode = "approve"
```
