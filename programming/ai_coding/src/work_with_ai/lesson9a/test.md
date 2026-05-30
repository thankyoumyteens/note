# 先在项目目录测试能否启动

进入你的项目目录：

```bash
cd /path/to/ai-doc-summary
```

先测试 MCP server 是否能运行：

```bash
npx -y @pimzino/spec-workflow-mcp@latest .
```

如果没有报错，说明包能拉取并启动。

但注意：这个命令本身是 MCP server，不是你平时直接交互的 CLI。MCP Server 的行为就像 Spring Boot 服务一样：启动后会在前台等待 MCP Client 通过 stdio 连接，所以终端看起来会“停住不动”。

实际使用时通常要让 Claude Code / Cursor / 其他 MCP Client 启动它。
