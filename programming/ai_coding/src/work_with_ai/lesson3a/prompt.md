# 本课推荐 Prompt

```text
目标：
为当前 ai-doc-summary 项目创建 WORKFLOW.md 初版，总结第 1～3 课形成的项目启动流程。

背景：
当前项目已经完成：
1. 第 1 课：从空目录创建最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：创建 AGENTS.md 和 CLAUDE.md 项目规则文件。
3. 第 3 课：创建 .gitignore 并建立 Git baseline commit。

现在进入第 3A 课：项目启动流程工具化。
本课目标是把当前项目启动经验沉淀为可复用的 WORKFLOW.md，而不是修改业务代码。

输入：
请查看当前项目结构、pom.xml、README.md、AGENTS.md、CLAUDE.md、.gitignore 和当前 git status。

输出：
请创建 WORKFLOW.md 初版，内容包括：

1. Project Bootstrap Workflow
   - 从空目录创建项目的标准步骤
   - 最小项目骨架要求
   - 不允许在启动阶段加入的内容

2. AI-Generated Project vs Spring Initializr
   - 什么时候适合让 AI 从空目录生成项目
   - 什么时候适合使用 Spring Initializr
   - 两者的优缺点

3. Maven Wrapper Notes
   - Maven Wrapper 的作用
   - 什么时候应该引入 Maven Wrapper
   - 当前项目是否建议立即引入，还是后续再考虑

4. Required Baseline Checklist
   - pom.xml
   - README.md
   - src/main/java
   - src/test/java
   - AGENTS.md
   - CLAUDE.md
   - .gitignore
   - mvn test
   - git status
   - baseline commit

5. Runtime / Port Checklist
   - mvn spring-boot:run 只用于验证启动
   - 验证后停止 Spring Boot 进程
   - 不要长期占用 8080
   - 8080 被占用时用 lsof -i tcp:8080 检查
   - 只停止监听 8080 的 Java/Spring Boot 进程

6. Recommended Commit Points
   - 项目骨架完成后提交
   - AGENTS.md / CLAUDE.md 完成后提交或合并进 baseline
   - .gitignore 确认后提交
   - 后续功能按小步提交

7. Reusable New Project Checklist
   - 下一个 Java 项目如何复用本流程

限制：
1. 不要修改 pom.xml。
2. 不要修改 Java 源码。
3. 不要修改测试代码。
4. 不要修改 README.md。
5. 不要修改 AGENTS.md 或 CLAUDE.md。
6. 不要新增依赖。
7. 不要引入数据库、Security、Docker、前端、真实 AI API 或 Spring AI。
8. 不要运行 mvn spring-boot:run。
9. 如需验证，只能运行 mvn test。
10. 不要执行 git add 或 git commit。
11. 不要创建复杂目录。
12. 本课只创建 WORKFLOW.md。

验收标准：
1. 根目录存在 WORKFLOW.md。
2. WORKFLOW.md 能说明 AI 生成项目和 Spring Initializr 的适用场景。
3. WORKFLOW.md 能说明 Maven Wrapper 的作用和引入时机。
4. WORKFLOW.md 包含项目启动 checklist。
5. WORKFLOW.md 包含 Git baseline checklist。
6. WORKFLOW.md 包含 8080 端口处理规则。
7. 没有修改业务代码、pom.xml、测试代码、README.md、AGENTS.md 或 CLAUDE.md。
8. 完成后请总结创建了哪些文件，以及后续如何使用 WORKFLOW.md。
```
