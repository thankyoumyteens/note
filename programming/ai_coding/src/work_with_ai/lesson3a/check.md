# 你要重点检查什么

## 检查 1：本课只应该新增 WORKFLOW.md

第 3A 课只允许新增：

```text
WORKFLOW.md
```

不应该改：

```text
pom.xml
src/main/java/...
src/test/java/...
README.md
AGENTS.md
CLAUDE.md
```

如果 Claude Code 改了这些文件，让它回退。

---

## 检查 2：不要马上引入 Maven Wrapper

本课是“理解和记录 Maven Wrapper”，不是一定要引入它。

如果 Claude Code 直接创建了：

```text
mvnw
mvnw.cmd
.mvn/wrapper/...
```

这不一定错，但超出了本课最小范围。

建议先让它记录：

```text
Maven Wrapper should be considered before the project is shared with teammates or CI.
Do not add Maven Wrapper in this lesson unless explicitly requested.
```

后面如果你决定引入，再单独做一次非平凡修改。

---

## 检查 3：Spring Initializr 不是替代当前项目

本课不是让你重建项目。

它只是让你理解：

```text
当前课程用 AI 从空目录生成项目，是为了训练 AI 指挥能力。
正式项目也可以用 Spring Initializr 先生成骨架，再让 AI 补规则文件和工作流。
```

所以 Claude Code 不应该重新生成项目，也不应该建议删除当前项目。
