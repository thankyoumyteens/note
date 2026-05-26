# 如果 Claude Code 误改了代码，怎么纠正

如果它改了 `pom.xml`、Java 源码、测试代码、README 或规则文件，发这个：

```text
第 3 课只允许检查 Git baseline 并创建或补充 .gitignore。
请不要修改 pom.xml、Java 源码、测试代码、README.md、AGENTS.md 或 CLAUDE.md。
请回退无关修改，只保留 .gitignore 的必要变更。
```
