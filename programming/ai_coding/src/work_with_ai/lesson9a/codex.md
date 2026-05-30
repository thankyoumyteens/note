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

如果多个项目都要用同一个 MCP，**不要给每个项目都复制一段固定绝对路径配置**。Codex 目前更适合用两种方式处理：

1. **全局配置一个“当前目录版” MCP**，让它以启动 Codex 的项目目录作为工作目录。
2. **为不同项目配置不同 MCP server 名称**，每个 server 写死一个项目路径。

优先推荐第 1 种。

---

### 方案 A：推荐，全局配置一个“当前项目的目录”

在 `~/.codex/config.toml` 里写：

```toml
[mcp_servers.spec-workflow]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "."
]
startup_timeout_sec = 20
```

然后你以后在哪个项目里启动 Codex，它就以哪个目录为项目目录：

```bash
cd /path/to/project-a
codex
```

```bash
cd /path/to/project-b
codex
```

Codex 的 MCP 配置通常放在 `~/.codex/config.toml`，使用 `[mcp_servers.<name>]` 配置 `command`、`args`、`env` 等字段；当前 Codex 的项目级 MCP 配置支持仍有一些讨论和限制，所以全局配置更稳。

---

### 方案 B：多个项目分别配置不同 server 名称

为每个项目写一个 server：

```toml
[mcp_servers.spec_workflow_learn_cc]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "/path1"
]
startup_timeout_sec = 20

[mcp_servers.spec_workflow_learn_codex]
command = "npx"
args = [
  "-y",
  "@pimzino/spec-workflow-mcp@latest",
  "/path2"
]
startup_timeout_sec = 20
```

缺点是：Codex 可能会在所有会话都加载这些 MCP server，工具列表会变乱，而且你要记住当前项目该用哪个 server。

所以这个方案适合少量固定项目，不适合很多项目。
