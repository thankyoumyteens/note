# Codex 完成后你自己执行的命令

Codex 做完后，你自己检查：

```bash
git status
```

然后跑测试：

```bash
mvn test
```

确认没有问题后，再提交：

```bash
git add .
git commit -m "chore: establish initial project baseline"
```

提交后检查：

```bash
git status
```

理想结果：

```text
nothing to commit, working tree clean
```
