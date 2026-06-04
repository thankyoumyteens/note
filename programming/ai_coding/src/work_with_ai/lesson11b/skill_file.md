# Skill 文件建议结构

每个 `SKILL.md` 可以用这个结构：

```markdown
# Skill: TDD Red

## Purpose

## When to use

## Inputs

## Steps

## Output format

## Hard rules

## Completion checklist

## Common mistakes to avoid
```

`SKILL.md` 不要写得太长。Skill 是给 AI 执行用的，不是论文。

## `SKILL.md` 格式要注意

为了同时兼容 Codex 和 Claude Code，建议每个 `SKILL.md` 的开头都写上 `name` 和 `description`。

例如：

```markdown
---
name: tdd-red
description: Use when starting a TDD Red phase for new behavior. Write failing tests only; do not implement production code.
---

# Skill: TDD Red

...
```
