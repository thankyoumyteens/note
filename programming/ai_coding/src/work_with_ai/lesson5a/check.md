# 你要重点检查什么

## 检查 1：有没有过度工具化

不值得工具化的 prompt：

```text
解释一个简单概念
临时问一个报错
一次性的文案修改
偶发的小问题
```

值得工具化的 prompt：

```text
新功能任务定义
diff review
handoff
spec 任务推进
测试失败分析
```

判断标准：

```text
高频
稳定
有固定输入
有固定输出
有明确验收标准
可以跨项目复用
```

---

## 检查 2：有没有提前创建复杂目录

第 5A 课不应该创建：

```text
.claude/
skills/
hooks/
```

如果 Claude Code 创建了这些目录，建议让它回退，只保留 `WORKFLOW.md` 更新。

纠正 Prompt：

```text
第 5A 课只要求在 WORKFLOW.md 中设计 Commands / Skills，不要求正式实现工具目录。

请回退 .claude/、skills/、hooks/ 等目录变更，只保留 WORKFLOW.md 的 Prompt Tooling 章节。
```

---

## 检查 3：有没有修改业务代码

本课只更新工作流文档，不应该修改：

```text
pom.xml
src/main/java/...
src/test/java/...
README.md
AGENTS.md
CLAUDE.md
```
