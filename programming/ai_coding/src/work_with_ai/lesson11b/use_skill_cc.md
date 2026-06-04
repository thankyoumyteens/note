# 把 Skill 安装到 Claude Code

个人级 Skills 放在 `~/.claude/skills/<skill-name>/SKILL.md`，项目级 Skills 放在 `.claude/skills/<skill-name>/SKILL.md`；可以自动触发，也可以用 `/skill-name` 直接调用。

## Claude Code 全局范围

适合场景：

```text
你希望所有 Claude Code 项目都能使用这些 TDD Skills。
```

目录结构：

```text
~/.claude/skills/
  tdd-red/
    SKILL.md
  tdd-green/
    SKILL.md
  tdd-refactor/
    SKILL.md
```

安装命令：

```bash
mkdir -p ~/.claude/skills

cp -R skills/tdd-red ~/.claude/skills/
cp -R skills/tdd-green ~/.claude/skills/
cp -R skills/tdd-refactor ~/.claude/skills/
```

进入任意项目启动 Claude Code：

```bash
claude
```

查看：

```text
/skills
```

### 直接调用：

```text
/tdd-red 为 PATCH /api/documents/{id}/title 先写失败测试，不要实现。
```

### 或者自然语言调用：

```text
使用 tdd-red skill，为 PATCH /api/documents/{id}/title 先写失败测试，不要实现。
```

---

## Claude Code 项目范围

适合场景：

```text
这些 TDD Skills 只属于当前项目，并且希望和项目一起提交。
```

项目根目录结构：

```text
ai-doc-summary/
  .claude/
    skills/
      tdd-red/
        SKILL.md
      tdd-green/
        SKILL.md
      tdd-refactor/
        SKILL.md
```

安装命令，在项目根目录执行：

```bash
mkdir -p .claude/skills

cp -R skills/tdd-red .claude/skills/
cp -R skills/tdd-green .claude/skills/
cp -R skills/tdd-refactor .claude/skills/
```

启动 Claude Code：

```bash
claude
```

查看：

```text
/skills
```
