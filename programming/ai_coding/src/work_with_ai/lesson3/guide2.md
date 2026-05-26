# 如果 Claude Code 自动 commit 了怎么办

本课要求它不要自动 commit，因为你要训练“人类确认 baseline”的习惯。

如果它已经 commit 了，不一定是严重错误，但要记录为问题。你可以检查：

```bash
git log --oneline -5
```

如果 commit 内容正确，可以保留；如果不正确，需要回滚。

最稳的第 3 课流程是：

```text
AI 检查和准备
人类 review
人类手动 git add / git commit
```
