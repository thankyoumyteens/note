# Claude Code 完成后你自己执行的命令

Claude Code 应该只帮你检查和创建 `.gitignore`，不要让它直接 commit。

你自己先看：

```bash
git status
```

再跑测试：

```bash
mvn test
```

确认没问题后手动提交：

```bash
git add .
git commit -m "chore: establish initial project baseline"
```

提交后再次检查：

```bash
git status
```

理想输出：

```text
nothing to commit, working tree clean
```

## 本课重点检查：target/ 不要提交

你运行过 `mvn test` 或 `mvn spring-boot:run` 后，本地通常会出现：

```text
target/
```

这是 Maven 构建产物，必须被 `.gitignore` 排除。

如果 `git status` 里出现：

```text
target/
```

说明 `.gitignore` 没配置好，不要提交。

你应该先确认 `.gitignore` 里有：

```gitignore
target/
```

然后再检查：

```bash
git status
```
