# Gemini CLI 配置 spec-workflow-mcp

Gemini CLI 支持两级配置，你可以根据自己的需求选择：

- 全局配置（推荐，所有项目生效）：
  - macOS / Linux: `~/.gemini/settings.json`
  - Windows: `%USERPROFILE%\.gemini\settings.json`
- 项目级配置（仅当前项目生效）：
  - 在你的项目根目录下创建 `.gemini/settings.json`

### 1. 添加 spec-workflow 配置

使用文本编辑器编辑 settings.json 该文件。

如果文件是新建的或者是空的，请直接粘贴以下内容。如果文件中已经有其他配置，找到或创建一个名为 mcpServers 的顶级字段并将 spec-workflow 补充进去：

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": ["-y", "@pimzino/spec-workflow-mcp@latest", "."],
      "env": {}
    }
  }
}
```

### 2. 启动并验证

配置保存后，在你的终端项目目录下直接启动 Gemini CLI。

进入交互界面后，你可以通过以下两种方式验证挂载是否成功：

- 运行内置命令： 输入 `/mcp list` 或者 `/mcp`，Gemini CLI 会打印出当前已成功连接的服务器状态。如果看到 `🟢 spec-workflow - Ready`，说明连接完美。
- 直接询问 Gemini： 对它说：“请列出你现在可用的外部工具。” 如果它回复包含 `mcp_spec-workflow_specs-workflow` 相关的函数，说明它已经可以帮你全自动生成架构规范和任务清单了。
