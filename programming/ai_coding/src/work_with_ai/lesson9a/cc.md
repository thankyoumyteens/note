# 配置到 Claude Code

常见方式是用 `claude mcp add`。

在 **项目目录** 执行：

```bash
claude mcp add spec-workflow -- npx -y @pimzino/spec-workflow-mcp@latest /path/to/ai-doc-summary
```

Claude Code 的 MCP add 常见格式就是 `claude mcp add <name> -- <command> <args...>`，`--` 后面的内容会作为 MCP server 的启动命令。

如果你的 Claude Code 对 `--` 后参数解析有问题，可以改用 JSON 配置方式。

配置后，在 Claude Code 里输入类似：

```text
请列出当前可用 MCP tools。
```

或者：

```text
请使用 spec-workflow MCP，显示当前项目的 specs。
```

如果能看到 spec workflow 相关工具，说明配置成功。

注意：`/path/to/ai-doc-summary` 要换成你自己的项目绝对路径，例如：

```bash
pwd
```

拿到当前目录后再填进去。

---

## MCP JSON 配置方式

项目级配置写在项目根目录的 `.mcp.json`。

用户级 / 本机级配置在 `~/.claude.json`。

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": [
        "-y",
        "@pimzino/spec-workflow-mcp@latest",
        "/path/to/ai-doc-summary"
      ]
    }
  }
}
```

如果你希望自动启动 Dashboard，有些版本支持类似参数：

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": [
        "-y",
        "@pimzino/spec-workflow-mcp@latest",
        "/path/to/ai-doc-summary",
        "--AutoStartDashboard"
      ]
    }
  }
}
```

不同 MCP Client 的配置文件位置不一样，所以这里不要硬背路径。原则是：

```text
command = npx
args = -y, @pimzino/spec-workflow-mcp@latest, 项目路径
```
