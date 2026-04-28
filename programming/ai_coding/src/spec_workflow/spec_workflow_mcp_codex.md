# Codex CLI 配置 spec-workflow-mcp

根据作用范围，你可以将配置写入以下两个位置：

- 全局配置：`~/.codex/config.toml`
- 项目级配置：在工作区根目录创建 `.codex/config.toml`（Codex 仅在“受信任的项目”中加载此文件，非常适合在特定项目中独立挂载工作流）。

### 1. 添加 spec-workflow 配置

按照 TOML 的层级追加到 config.toml 文件末尾：

```ini
# 声明一个名为 spec-workflow 的 MCP 服务器
[mcp_servers.spec-workflow]
command = "npx"
args = ["-y", "@pimzino/spec-workflow-mcp@latest", "."]
enabled = true
```

### 2. 启动并验证

配置保存后，在你的终端项目目录下直接启动 Codex CLI。

进入交互界面后，你可以通过以下两种方式验证挂载是否成功：

- 运行内置命令： 输入 `/mcp list` 或者 `/mcp`，Codex CLI 会打印出当前已成功连接的服务器状态。如果看到 `🟢 spec-workflow - Ready`，说明连接完美。
- 直接询问 Codex： 对它说：“请列出你现在可用的外部工具。” 如果它回复包含 `mcp_spec-workflow_specs-workflow` 相关的函数，说明它已经可以帮你全自动生成架构规范和任务清单了。
