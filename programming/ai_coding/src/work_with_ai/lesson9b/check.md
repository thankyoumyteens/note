# 本课开始前检查

先确认你在项目根目录：

```bash
pwd
```

检查当前状态：

```bash
git status
```

检查 MCP 是否配置好：

Claude Code：

```bash
claude mcp list
```

Codex：

```bash
cat ~/.codex/config.toml
```

如果用 Dashboard，可以启动：

```bash
npx -y @pimzino/spec-workflow-mcp@latest . --dashboard
```
