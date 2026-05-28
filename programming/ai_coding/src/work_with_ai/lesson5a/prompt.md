# 本课推荐 Prompt

```text
目标：
为当前 ai-doc-summary 项目设计 Prompt 模板工具化方案，重点设计 Commands / Skills，但本课不正式实现复杂工具。

背景：
当前项目已经完成：
1. 第 1 课：最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：AGENTS.md / CLAUDE.md 项目规则文件。
3. 第 3 课：.gitignore 和 Git baseline commit。
4. 第 3A 课：WORKFLOW.md 初版。
5. 第 4 课：将“文档保存功能”改写为清晰任务。
6. 第 5 课：围绕文档保存功能练习输出格式控制。

现在进入第 5A 课：Prompt 模板工具化：Commands / Skills。
本课目标是判断哪些高频 prompt 值得工具化，并设计 3 个项目级可复用命令或技能：
1. new-feature-task
2. review-diff
3. write-handoff

输入：
请查看当前项目结构、AGENTS.md、CLAUDE.md、WORKFLOW.md、README.md 和当前 git status。

输出：
请不要修改业务代码。
请不要创建 .claude/、skills/、hooks/ 等复杂目录。
请只更新 WORKFLOW.md，新增一个章节：

## Prompt Tooling: Commands and Skills

该章节需要包含：

1. When to Tool a Prompt
   - 哪些 prompt 值得工具化
   - 哪些 prompt 不值得工具化
   - 如何避免过度工具化

2. Command vs Skill
   - Command 适合什么
   - Skill 适合什么
   - 当前项目早期阶段应该优先设计哪些

3. new-feature-task
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构

4. review-diff
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构

5. write-handoff
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构

6. Future Implementation Notes
   - 后续如何迁移到 Claude Slash Commands
   - 后续如何迁移到 Claude Skills
   - 后续如何迁移到 Codex Skills
   - 当前为什么只记录设计，不创建正式工具目录

限制：
1. 不要修改 pom.xml。
2. 不要修改 Java 源码。
3. 不要修改测试代码。
4. 不要修改 README.md。
5. 不要修改 AGENTS.md 或 CLAUDE.md。
6. 不要新增依赖。
7. 不要创建 .claude/ 目录。
8. 不要创建 skills/ 目录。
9. 不要创建 hooks/ 目录。
10. 不要运行 mvn spring-boot:run。
11. 如果需要验证，只能运行 mvn test。
12. 不要执行 git add 或 git commit。
13. 不要实现文档保存功能。
14. 不要接入数据库、Spring AI、真实 AI API、Security、用户系统或文件上传。

验收标准：
1. WORKFLOW.md 中新增 Prompt Tooling: Commands and Skills 章节。
2. 章节中明确说明什么时候值得工具化 prompt。
3. 章节中明确区分 Command 和 Skill。
4. 包含 new-feature-task 的设计。
5. 包含 review-diff 的设计。
6. 包含 write-handoff 的设计。
7. 明确当前不创建 .claude/、skills/、hooks/ 目录。
8. 没有修改业务代码。
9. 没有新增依赖。
10. 完成后总结修改了哪些文件，以及后续如何使用。
```
