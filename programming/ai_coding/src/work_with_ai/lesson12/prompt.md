# 本课推荐 Prompt

```text
目标：
设计当前项目的最小 Hooks 自动化策略。

任务目标：
当前项目已经有 TDD Skills、spec-tdd-cycle Skill、spec-workflow-mcp、AGENTS.md、CLAUDE.md 和 WORKFLOW.md。
现在需要设计一组最小、低风险的 Codex Hooks 与 Claude Code Hooks，用于提醒测试、拦截高风险命令，并减少 AI 自动化开发中的常见失误。

本任务先只做设计评估。
不要创建 Hook 配置文件。
不要修改项目文件。
不要实现新业务功能。
不要修改 Java 代码。
不要修改测试代码。

请先读取：
1. AGENTS.md
2. CLAUDE.md
3. WORKFLOW.md
4. skills/ 目录
5. 当前 Codex Hooks 状态
6. 当前 Claude Code Hooks 状态或 .claude 配置
7. 当前 git status

第一步：
请先输出 Hooks 设计评估报告：

1. 当前项目有哪些规则适合用 Hook 自动提醒或拦截。
2. 哪些规则适合放到 Codex PreToolUse。
3. 哪些规则适合放到 Codex PostToolUse。
4. 哪些规则适合放到 Codex Stop。
5. 哪些规则适合放到 Claude Code PreToolUse。
6. 哪些规则适合放到 Claude Code PostToolUse。
7. 哪些规则适合放到 Claude Code Stop。
8. 哪些规则仍然应该保留在 AGENTS.md / CLAUDE.md / Skill hard rules 中。
9. 哪些场景不应该自动化。
10. 是否建议创建 docs/hooks.md。
11. 是否建议创建 Codex hooks 配置。
12. 是否建议创建 Claude Code hooks 配置。
13. 哪些配置适合项目级提交。
14. 哪些配置只适合本地。
15. 是否存在误拦截或过度自动化风险。

等我确认后，再修改文件。

建议的最小 Hook 策略：

1. PreToolUse：
   - 对 git add / git commit 做提醒或阻止。
   - 对 mvn spring-boot:run 做提醒，避免长期占用端口。
   - 对明显危险命令做提醒或阻止。

2. PostToolUse：
   - 如果修改了 src/main/java 或 src/test/java，提醒运行 mvn test。
   - 如果修改了 pom.xml，提醒说明是否新增依赖。

3. Stop：
   - 本轮结束前提醒输出：
     - 修改了哪些文件
     - 是否运行测试
     - 测试结果
     - git status 摘要
     - git diff --stat 摘要
     - 是否有越界修改

允许后续新增：
1. docs/hooks.md
2. Codex hooks 配置文件，具体路径必须先说明并等待确认
3. Claude Code hooks 配置文件，具体路径必须先说明并等待确认

允许后续小幅修改：
1. WORKFLOW.md
2. AGENTS.md
3. CLAUDE.md

修改要求：
1. docs/hooks.md 记录项目 Hook 策略。
2. WORKFLOW.md 只添加 Hooks 索引和选择规则，不写长篇教程。
3. AGENTS.md / CLAUDE.md 只添加稳定、简短、必须默认遵守的 hook-like fallback rules。
4. 不要使用课程化描述。
5. 不要引用课程文件。
6. 不要引入复杂自动化。
7. 不要自动运行测试，除非用户明确允许。
8. 不要自动执行 git add 或 git commit。
9. Codex Hooks 和 Claude Code Hooks 要分开记录，不要混成一种配置。
10. 创建任何 Hook 配置前，必须先说明：
    - 配置路径
    - 作用域
    - 是否应提交 Git
    - 触发事件
    - 匹配规则
    - 执行动作
    - 误拦截风险

禁止修改：
1. 不修改 src/main/java
2. 不修改 src/test/java
3. 不修改 pom.xml
4. 不新增依赖
5. 不实现新接口
6. 不修改已有接口行为
7. 不接真实 AI API
8. 不接 Spring AI
9. 不接数据库 / JPA
10. 不加入 Spring Security / 用户系统
11. 不运行 mvn spring-boot:run
12. 不执行 git add
13. 不执行 git commit

完成设计评估后输出：
1. 是否确认 Codex 支持 Hooks。
2. Codex 当前已安装 / 激活 Hooks 数量。
3. Claude Code 当前 Hooks 配置状态。
4. 推荐的最小 Hook 列表。
5. 哪些 Hook 是提醒型。
6. 哪些 Hook 是拦截型。
7. 哪些 Hook 不建议现在实现。
8. 建议新增或修改哪些文件。
9. 是否建议先只创建 docs/hooks.md。
10. 是否建议暂缓真实 Hook 配置。
11. git status 摘要。
12. 等待用户确认。
```

## 评估报告示例

```
Hooks 设计评估报告

  已完成只读检查：AGENTS.md、CLAUDE.md、WORKFLOW.md、skills/、项目级 .claude、全
  局 Codex/Claude 配置、git status。未修改文件，未运行 mvn spring-boot:run，未执
  行 git add / git commit。

  1. 适合 Hook 自动提醒或拦截的项目规则

  - 提醒：Java/test/pom 修改后提示运行 mvn test。
  - 提醒：pom.xml 修改后提示说明是否新增依赖。
  - 提醒：mvn spring-boot:run 可能长期占用 8080，结束后要停止进程。
  - 拦截或强提醒：git add、git commit，除非用户明确要求。
  - 拦截：明显危险命令，例如 git reset --hard、git checkout --、删除项目目录、修
    改认证/密钥文件。

  - 提醒：Stop 前输出 changed files、测试状态、git status、git diff --stat、是否
    越界修改。

  2. 适合 Codex PreToolUse

  - git add / git commit：默认阻止或要求明确确认。
  - git reset --hard、git checkout --、大范围 rm：阻止。
  - mvn spring-boot:run：提醒端口和停止进程，不建议直接阻止。
  - 修改 pom.xml：提醒依赖变更需要用户确认。
  - 修改 src/main/java、src/test/java：提醒必须符合当前任务和 TDD phase。

  3. 适合 Codex PostToolUse

  - 检测到 src/main/java 或 src/test/java 变更后，提醒运行 mvn test。
  - 检测到 pom.xml 变更后，提醒报告依赖变化。
  - 检测到 forbidden surface 变更，例如数据库、安全、Docker、前端目录，提醒越界
    风险。

  - 命令执行后如果启动了 Spring Boot，提醒确认进程已停止。

  4. 适合 Codex Stop

  - 强制结束摘要检查：
      - 修改了哪些文件。
      - 是否运行测试。
      - 测试结果。
      - git status 摘要。
      - git diff --stat 摘要。
      - 是否修改了禁止区域。

  - 只做提醒，不自动运行测试、不自动提交。

  5. 适合 Claude Code PreToolUse

  - 与 Codex 类似，但单独配置：
      - 拦截 git add / git commit。
      - 拦截危险 git/删除命令。
      - 提醒 mvn spring-boot:run。
      - 提醒 pom.xml 修改需要显式依赖说明。
      - 提醒 TDD phase 边界。

  6. 适合 Claude Code PostToolUse

  - Java/test 变更后提醒 mvn test。
  - pom.xml 变更后提醒依赖说明。
  - 启动命令后提醒不要遗留 Java/Spring Boot 进程。
  - 越界目录或禁止技术栈出现时提醒人工检查。

  7. 适合 Claude Code Stop

  - 与 Codex Stop 保持一致：
      - changed files。
      - verification。
      - test result。
      - git status。
      - diff stat。
      - out-of-scope check。

  8. 应继续保留在 AGENTS.md / CLAUDE.md / Skills 的规则

  - TDD Red/Green/Refactor phase 边界。
  - spec-tdd-cycle 的一轮一停、一任务一停。
  - 不引入数据库、Security、Docker、Spring AI、真实 AI API、用户系统。
  - 行为变更必须有测试。
  - 不修改无关文件。
  - 不新增依赖，除非用户明确确认。
  - Hook 只能辅助提醒，不能替代 Skill hard rules。

  9. 不应该自动化的场景

  - 自动运行 mvn test：用户已明确要求不要默认自动运行。
  - 自动执行 git add / git commit。
  - 自动停止端口 8080 上的进程。
  - 自动判断并修改 TDD phase。
  - 自动创建 spec、实现功能、修复测试。
  - 自动修改 pom.xml 或添加依赖。
  - 自动扫描/输出敏感配置内容。

  10. 是否建议创建 docs/hooks.md

  - 建议。
  - 它适合作为项目级 Hook 策略说明，不会改变运行行为，风险最低。
  - 建议先只创建这个文件，等策略稳定后再创建真实 Hook 配置。

  11. 是否建议创建 Codex hooks 配置

  - 建议暂缓。
  - 当前已确认 Codex 支持 Hook events，但项目内没有 .codex 配置。
  - 真实配置路径、作用域、是否提交 Git，需要先单独确认。

  12. 是否建议创建 Claude Code hooks 配置

  - 建议暂缓。
  - 当前项目级 .claude 只有 skill，没有发现 project settings/hooks。
  - 全局 Claude settings 存在，但属于本地配置，不建议作为项目提交对象。

  13. 适合项目级提交的配置

  - docs/hooks.md。
  - 轻量索引：WORKFLOW.md 增加 Hooks 索引和选择规则。
  - 简短 fallback rules：AGENTS.md / CLAUDE.md 增加稳定、必须遵守的 hook-like 规
    则。

  - 若后续创建项目级 Claude hooks，可考虑 .claude/settings.json，但需确认是否符
    合团队使用方式。

  14. 只适合本地的配置

  - ~/.codex/config.toml 中的 Codex 全局配置。
  - ~/.claude/settings.json 中的 Claude 全局配置。
  - 任何包含环境变量、token、个人路径、模型代理地址的配置。
  - 个体开发者偏好的本地 hook 脚本。

  15. 误拦截或过度自动化风险

  - git add / git commit 完全阻止可能影响用户明确要求提交的场景，建议“默认阻止，
    用户明确允许后放行”。

  - mvn spring-boot:run 阻止过强，建议提醒型。
  - Java/test 修改后强制测试可能打断 Red phase，因为 Red 期望测试失败，建议提醒
    型。

  - pom.xml 修改不一定是新增依赖，也可能是插件或版本整理，建议提醒说明而非阻止。
  - Stop hook 如果内容太长，会变成噪音，建议固定短摘要。

  当前状态

  - Codex 是否支持 Hooks：是，基于你已确认的 events 列表。
  - Codex 当前已安装 / 激活 Hooks 数量：当前检查到 ~/.codex/config.toml 无 hooks
    配置；项目内无 .codex 目录。按现有可见配置计为 0。

  - Claude Code 当前 Hooks 配置状态：项目级 .claude 未发现 settings/hooks；全局
    ~/.claude/settings.json 未发现 hooks 字段。

  - git status 摘要：当前在 main 分支，git status --short 无输出，工作区 clean。
  - git diff --stat 摘要：无输出，当前没有 diff。

  推荐最小 Hook 列表

  提醒型：

  - PreToolUse：mvn spring-boot:run 提醒端口和进程清理。
  - PostToolUse：Java/test 变更提醒 mvn test。
  - PostToolUse：pom.xml 变更提醒说明依赖。
  - Stop：提醒输出变更、测试、git status、diff stat、越界检查。

  拦截型：

  - PreToolUse：阻止或要求确认 git add / git commit。
  - PreToolUse：阻止危险 git/删除命令。
  - PreToolUse：阻止明显修改敏感配置或越权路径的命令。

  暂不建议现在实现：

  - 自动运行测试。
  - 自动启动/停止 Spring Boot。
  - 自动提交。
  - 自动修复越界修改。
  - 自动执行复杂 spec/TDD 状态机判断。

  建议下一步先只创建 docs/hooks.md，暂缓真实 Codex/Claude Hook 配置。等你确认
  后，我再说明每个拟创建配置的路径、作用域、是否提交 Git、触发事件、匹配规则、执
  行动作和误拦截风险，然后再修改文件。
```

## 创建 docs/hooks.md

```
继续。

只执行下一步：创建 docs/hooks.md，记录当前项目的 Hooks 策略。
不要创建 Codex hooks 配置。
不要创建 Claude Code hooks 配置。
不要修改 Java 代码。
不要修改测试代码。
不要修改 pom.xml。
不要执行 git add 或 git commit。

docs/hooks.md 应包含：
1. Purpose
2. Hook vs Skill
3. Codex Hooks
4. Claude Code Hooks
5. Reminder hooks
6. Blocking hooks
7. What not to automate
8. Minimal hook strategy for this project
9. Current decision: create docs/hooks.md first, defer real hook configuration
10. Future configuration checklist

完成后输出：
1. 创建/修改了哪些文件。
2. docs/hooks.md 记录了哪些内容。
3. 是否创建 Codex hooks 配置。
4. 是否创建 Claude Code hooks 配置。
5. 是否修改 AGENTS.md / CLAUDE.md / WORKFLOW.md。
6. 是否修改 src/main/java。
7. 是否修改 src/test/java。
8. 是否修改 pom.xml。
9. git status 摘要。
10. git diff --stat 摘要。
```

这一步只应该产生：

```
docs/hooks.md
```

## 让 AI 审查 docs/hooks.md 内容

```
继续。

只执行下一步：审查 docs/hooks.md。
不要修改任何文件。
不要创建 Codex hooks 配置。
不要创建 Claude Code hooks 配置。
不要修改 AGENTS.md / CLAUDE.md / WORKFLOW.md。
不要修改 Java 代码、测试代码或 pom.xml。

请检查：
1. docs/hooks.md 是否清楚区分 Hook 和 Skill。
2. 是否分别说明 Codex Hooks 和 Claude Code Hooks。
3. 是否明确当前只做文档，不创建真实配置。
4. 是否避免自动运行 mvn test。
5. 是否避免自动 git add / git commit。
6. 是否避免过度自动化。
7. 是否有不准确或容易误导的描述。
8. 是否需要删减内容。

完成后只输出审查意见：
1. 是否通过。
2. 是否建议修改。
3. 如果建议修改，列出最小修改点。
4. 不要直接修改文件。
```
