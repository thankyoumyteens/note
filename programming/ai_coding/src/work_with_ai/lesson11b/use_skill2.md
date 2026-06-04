# 在 AGENTS.md / CLAUDE.md 里加“自动使用规则”

在 AGENTS.md / CLAUDE.md 里加一小段：

```markdown
## TDD Skill Usage

For behavior changes, prefer the TDD skills:

- Use `skills/tdd-red/SKILL.md` when defining new expected behavior with tests.
- Use `skills/tdd-green/SKILL.md` when making failing tests pass.
- Use `skills/tdd-refactor/SKILL.md` after tests pass and cleanup may be needed.

Rules:

- Do not write production code during Red.
- Do not delete tests or weaken assertions during Green.
- Do not change API behavior during Refactor.
- If unsure which phase applies, ask for clarification or explain the phase choice before editing.
```

## 这样以后你可以

```
新增 PATCH /api/documents/{id}/title。按项目 TDD Skill 规则走 Red 阶段，先写失败测试，不要实现。
```

```
Red 已完成。按项目 TDD Skill 规则走 Green 阶段，写最小实现让测试通过。
```

```
Green 已完成。按项目 TDD Skill 规则走 Refactor 阶段，先评估是否需要重构。
```

AI 就应该知道去读对应 Skill。
