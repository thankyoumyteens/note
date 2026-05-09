# 第 3 课：初始化 Git 与基线提交

## 这一课要解决什么问题

你现在已经有：

```text
Spring Boot 最小项目
AGENTS.md
CLAUDE.md
lessons/lesson-02-project-rules.md
README.md
pom.xml
src/
```

但如果还没有干净的 Git baseline，后面 AI 一旦乱改，你很难判断：

```text
哪些是原始项目文件？
哪些是第 2 课新增的规则文件？
哪些是 AI 后续误改的？
哪些可以安全回滚？
```

所以第 3 课要做三件事：

```text
1. 检查项目是否干净
2. 创建或修正 .gitignore
3. 建立第一次 baseline commit
```
