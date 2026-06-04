# 显式告诉 AI 使用某个 Skill

比如你要给新功能先写测试，就对 Codex / Claude Code 说：

```
请使用 skills/tdd-red/SKILL.md。

目标：
为 PATCH /api/documents/{id}/title 先写失败测试，不要实现功能。

请严格遵守该 Skill：
1. 只允许修改测试文件
2. 不允许修改 src/main/java
3. 写完后运行测试
4. 说明失败原因是否符合预期
```

## 第 Red 阶段测试已经失败后，用：

```
请使用 skills/tdd-green/SKILL.md。

背景：
第 Red 阶段已经为 PATCH /api/documents/{id}/title 写好了失败测试。
失败原因是接口尚未实现。

目标：
写最小实现，让现有失败测试通过。

限制：
1. 不降低测试断言
2. 不删除测试
3. 不扩大功能范围
4. 不修改 pom.xml
5. 不新增依赖
6. 不接数据库 / JPA / Spring AI / 真实 AI API
7. 完成后运行 mvn test
```

## 测试通过后，用：

```
请使用 skills/tdd-refactor/SKILL.md。

背景：
PATCH /api/documents/{id}/title 的 Red 和 Green 阶段已完成，mvn test 通过。

目标：
先评估是否需要重构。
如果不需要，请说明原因并停止。
如果需要，只做小步、行为不变的重构。

限制：
1. 不新增业务功能
2. 不修改 API 行为
3. 不降低测试断言
4. 不删除测试
5. 每步后运行测试
```
