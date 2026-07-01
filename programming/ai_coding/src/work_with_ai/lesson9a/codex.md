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

目前只能去修改 "/path/to/ai-doc-summary"。
