# 使用 Skill

目前最稳的用法有四种，按推荐顺序：

1. 原生 Skill 调用：把 Skill 安装到工具可发现目录，然后用 /skills 或 skill 名称调用
2. 项目规则触发：在 AGENTS.md / CLAUDE.md 里规定什么时候必须使用哪个 Skill
3. 显式路径调用：当自动发现不稳定时，直接要求 AI 读取某个 SKILL.md
4. 命令封装：后续可以把常用 Skill 包成 slash command
