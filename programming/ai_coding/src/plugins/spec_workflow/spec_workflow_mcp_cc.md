# Claude Code 配置 spec-workflow-mcp

常见方式是用 `claude mcp add`。

在项目目录执行：

```bash
claude mcp add spec-workflow -- npx -y @pimzino/spec-workflow-mcp@latest /path/to/your/project
```

## 通过配置文件配置

也可以通过配置 `.mcp.json` 文件实现。

`.mcp.json` 文件可以写到两个地方：

1. 用户的主目录：提供通用的工具和环境变量
2. 特定项目的根目录：提供仅对当前项目生效的特定工具

Claude Code 会先读取 主目录的全局配置 (`~/.mcp.json`) 作为底座，然后再读取 当前项目的局部配置 (`./.mcp.json`)。主目录全局配置的优先级高于项目目录。

```json
{
  "mcpServers": {
    "spec-workflow": {
      "command": "npx",
      "args": [
        "-y",
        "@pimzino/spec-workflow-mcp@latest",
        "/path/to/your/project"
      ]
    }
  }
}
```
