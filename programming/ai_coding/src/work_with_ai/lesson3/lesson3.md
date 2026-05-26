# 第 3 课：初始化 Git 与基线提交

你现在已经完成：

```text
第 1 课：最小 Spring Boot 项目
第 2 课：AGENTS.md / CLAUDE.md 项目规则文件
```

第 3 课要做的是：

```text
1. 检查当前项目状态
2. 创建或修正 .gitignore
3. 确认 target/ 等构建产物不会被提交
4. 运行 mvn test
5. 建立第一个 baseline commit
```

这个 baseline commit 很重要。后面 AI 写代码、重构、生成 spec、改测试时，如果出问题，你可以随时回到这个干净起点。

## 为什么 AI 项目必须先有 Git baseline

AI coding agent 很容易一次性修改多个文件。没有 Git baseline 时，你很难判断：

```text
哪些文件是项目原始骨架？
哪些是 AGENTS.md / CLAUDE.md？
哪些是 AI 后来误改的？
哪些可以安全回滚？
```

有 baseline 之后，你可以用：

```bash
git status
git diff
git restore <file>
git reset --hard HEAD
```

来控制风险。

注意：`git reset --hard HEAD` 会丢弃所有未提交修改，只有你明确要全部回滚时才用。
