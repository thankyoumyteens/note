# 它可能生成什么目录

工具可能在项目下生成类似：

```text
.spec-workflow/
  specs/
  approvals/
  archive/
  steering/
  templates/
  user-templates/
```

不同版本可能略有差异。

处理原则：

```text
1. 不要一生成就全部提交
2. 先看里面是什么
3. spec 正文、任务、steering 文档通常可能适合提交
4. 本地缓存、临时日志、机器相关状态不一定适合提交
5. 先用 git status / git diff 看清楚
```

建议第 9A 课先不要 commit：

```bash
git status
git diff --stat
```

如果你还不确定 `.spec-workflow/` 是否提交，可以先让它保留在工作区，等第 9B 课实践后再决定 `.gitignore` 策略。
