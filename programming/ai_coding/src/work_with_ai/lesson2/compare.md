# AGENTS.md 和 CLAUDE.md 的区别

## AGENTS.md

偏工具中立，优先给 Codex / Codex CLI 使用。

它应该包含：

```text
项目定位
技术栈
命令
代码规则
工作流规则
安全规则
Review checklist
```

## CLAUDE.md

给 Claude Code 使用。

除了包含 AGENTS.md 的核心规则外，还可以加一些 Claude Code 相关约束，例如：

```text
先 Explore / Plan，再改代码
不要长期运行服务
运行 mvn spring-boot:run 后要停止进程
长任务结束后生成 handoff
未来可以接入 MCP / Skills / Hooks
```
