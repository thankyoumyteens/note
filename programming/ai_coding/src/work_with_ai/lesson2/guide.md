# 重点观察 AI 有没有犯这些错误

## 错误 1：趁机改代码

第 2 课只创建规则文件，不应该改：

```text
pom.xml
src/main/java/...
src/test/java/...
```

如果 Codex 修改了这些文件，你要让它回退。

纠正 prompt：

```text
第 2 课只允许创建 AGENTS.md、CLAUDE.md 和 lessons/lesson-02-project-rules.md。
请不要修改 pom.xml、Java 源码或测试。
请回退无关修改，只保留规则文件和课程笔记。
```

---

## 错误 2：规则写得太虚

差的规则：

```text
写高质量代码
注意安全
保持简洁
```

好的规则：

```text
- Do not add dependencies without explicit approval.
- Add or update tests for behavior changes.
- For non-trivial changes, propose a plan before editing.
- Do not hardcode API keys, secrets, tokens, or credentials.
- Run mvn test after code changes when practical.
```

规则必须能约束 AI 的行为。

---

## 错误 3：过早引入复杂技术

现在不应该写成：

```text
必须使用 PostgreSQL
必须使用 Docker
必须使用 Spring Security
必须使用 Redis
必须接入 OpenAI
```

现在应该写：

```text
H2 may be introduced later for early persistence lessons.
PostgreSQL may be introduced later.
External AI providers will be introduced later through an abstraction.
```

也就是：**允许后续引入，但现在不默认引入。**
