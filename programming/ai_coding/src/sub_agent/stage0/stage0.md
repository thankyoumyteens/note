# 阶段 0：项目级上下文校准

1. 第 1 轮：AI 直接分析项目并创建 6 个文件:
   - .spec-workflow/steering/product.md
   - .spec-workflow/steering/tech.md
   - .spec-workflow/steering/structure.md
   - AGENTS.md
   - docs/lessons/README.md
   - docs/decisions/README.md
2. 第 2 轮：你看文件后，指出要改哪里，AI 只改指定文件

## 先建立一个分支

在项目根目录执行：

```bash
git checkout -b workflow/stage-0-context
```

然后确认项目当前干净：

```bash
git status
./mvnw test
```

如果测试本来就不过，先记录，不要让 AI 直接修。
