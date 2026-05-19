# 重点观察 AI 有没有犯这些错误

完成后重点检查 4 类问题。

## 检查 1：有没有乱改代码

第 2 课只允许新增：

```text
AGENTS.md
CLAUDE.md
```

不应该修改：

```text
pom.xml
src/main/java/...
src/test/java/...
README.md
```

如果 Claude Code 改了业务代码，让它回退。

纠正 Prompt：

```text
第 2 课只允许创建 AGENTS.md 和 CLAUDE.md。
请不要修改 pom.xml、Java 源码、测试代码或 README.md。
请回退无关修改，只保留 AGENTS.md 和 CLAUDE.md。
```

---

## 检查 2：规则是否太虚

不好的规则：

```text
Write good code.
Keep code clean.
Be careful.
```

好的规则：

```text
Do not add dependencies without explicit approval.
For non-trivial changes, propose a plan before editing.
Add or update tests for behavior changes.
Run mvn test after code changes when practical.
Do not hardcode secrets, tokens, API keys, or credentials.
Stop Spring Boot after verifying mvn spring-boot:run.
```

规则必须能约束 AI 的行为。

---

## 检查 3：有没有记住“不接真实 AI”

因为本课重点是 **AI 工具驱动开发工作流**，不是 Java AI Provider / Spring AI 接入。

所以规则里应该明确：

```text
Do not add Spring AI.
Do not connect to real AI APIs.
Fake AI clients may be used later only for TDD and workflow exercises.
```

---

## 检查 4：有没有写入 8080 端口规则

```text
When running mvn spring-boot:run, stop the process after verification.
Do not leave Java processes occupying port 8080.
If port 8080 is occupied, use lsof -i tcp:8080 to identify the process.
Stop only the Java/Spring Boot process that is listening on 8080.
```

这个很实用，后续会减少重复排查。
