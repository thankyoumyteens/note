# 第 2 课：建立项目规则文件 `AGENTS.md` / `CLAUDE.md`

## 这一课要解决什么问题

现在项目已经能跑，但 AI 还不知道你的长期规则。

如果你每次都临时告诉 AI：

```text
这是 Java 21 项目
不要乱加依赖
不要加数据库
不要加 Security
每次改完要跑测试
不要硬编码 API key
```

会很麻烦，也容易漏。

所以第 2 课要把这些规则写进项目根目录：

```text
AGENTS.md
CLAUDE.md
```

作用是：

```text
AGENTS.md  → 给 Codex / Codex CLI 使用
CLAUDE.md  → 给 Claude Code 使用
```

## 这两个文件应该写什么

它们不是项目说明书，也不是 README。

它们是给 AI coding agent 看的“工作规则”。

核心内容应该包括：

```text
1. 项目定位
2. 技术栈
3. 常用命令
4. 代码规则
5. 工作流规则
6. 安全规则
7. Review 标准
```
