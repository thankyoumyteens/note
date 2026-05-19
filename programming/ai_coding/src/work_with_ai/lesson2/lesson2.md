# 第 2 课：建立项目规则文件 `AGENTS.md` / `CLAUDE.md`

现在你已经有了最小 Spring Boot 项目。第 2 课要做的是：

```text
为项目建立 AI agent 的长期规则文件：
1. AGENTS.md
2. CLAUDE.md
```

这两个文件的作用不是给人看的普通 README，而是给 AI coding agent 看的项目规则。

它们要告诉 Codex / Claude Code：

```text
这个项目是什么
技术栈是什么
能做什么
不能做什么
测试命令是什么
启动命令是什么
修改代码前要怎么计划
修改代码后要怎么验证
运行 Spring Boot 后要不要停止进程
```

## 为什么第 2 课很重要

如果没有规则文件，你每次都要重复告诉 AI：

```text
不要加数据库
不要加 Spring Security
不要加 Spring AI
不要接真实 AI API
不要乱加依赖
不要长期占用 8080
修改代码后要跑测试
```

这很低效，也容易漏。

规则文件的价值是：

> 把你反复强调的项目纪律写进仓库，让 AI 每次进入项目时都能先读规则。
