# 把 Skill 安装到 Codex

Codex 会从 repository、user、admin、system 等位置读取 Skills；用户级是 `$HOME/.agents/skills`，项目级会扫描当前目录到 repo root 之间的 `.agents/skills`。Codex 的 Skill 是包含 `SKILL.md` 的目录，`SKILL.md` 必须包含 `name` 和 `description`。

## Codex 全局范围

适合场景：

```text
你希望所有项目都能使用 tdd-red / tdd-green / tdd-refactor。
```

目录结构：

```text
~/.agents/skills/
  tdd-red/
    SKILL.md
  tdd-green/
    SKILL.md
  tdd-refactor/
    SKILL.md
```

安装命令：

```bash
mkdir -p ~/.agents/skills

cp -R skills/tdd-red ~/.agents/skills/
cp -R skills/tdd-green ~/.agents/skills/
cp -R skills/tdd-refactor ~/.agents/skills/
```

然后进入任意项目启动 Codex：

```bash
codex
```

查看：

```text
/skills
```

### 显式调用：

```text
$tdd-red 为 PATCH /api/documents/{id}/title 先写失败测试，不要实现。
```

### 也可以直接说：

```text
使用 tdd-red skill，为 PATCH /api/documents/{id}/title 先写失败测试，不要实现。
```

Codex 支持两种激活方式：

1. 显式调用，也就是在 CLI/IDE 中运行 `/skills` 或输入 `$` mention 一个 skill
2. 以及隐式调用，也就是任务描述匹配 skill 的 `description` 时自动选择。

---

## Codex 项目范围

适合场景：

```text
这些 TDD Skills 只服务于当前 ai-doc-summary 项目。
```

项目根目录结构：

```text
ai-doc-summary/
  .agents/
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
mkdir -p .agents/skills

cp -R skills/tdd-red .agents/skills/
cp -R skills/tdd-green .agents/skills/
cp -R skills/tdd-refactor .agents/skills/
```

然后从项目根目录启动 Codex：

```bash
codex
```

查看：

```text
/skills
```

如果没显示，重启 Codex。

## 建议提交 Git 吗？

```text
项目级 .agents/skills/ 可以提交。
全局 ~/.agents/skills/ 不提交。
```
