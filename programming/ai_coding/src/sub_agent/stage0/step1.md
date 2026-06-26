# 创建文档

先把下面这段直接丢给 AI。

```
阶段 0：项目级上下文校准。

目标：分析当前 spring-petclinic-rest 项目，并创建项目级上下文文件。

必须创建或更新以下文件：

* .spec-workflow/steering/product.md
* .spec-workflow/steering/tech.md
* .spec-workflow/steering/structure.md
* AGENTS.md
* docs/lessons/README.md
* docs/decisions/README.md

要求：

1. 先读取项目事实：

   * README.md
   * pom.xml
   * src/main/java
   * src/main/resources
   * src/test/java
   * OpenAPI / Swagger 配置
   * 数据库初始化脚本
   * 测试配置

2. steering 三个文件优先使用 MCP 暴露的 steering 创建/更新工具；如果当前会话没有暴露该工具，则按 steering_guide 创建/更新 steering markdown 文件：

   * product
   * tech
   * structure

3. AGENTS.md、docs/lessons/README.md、docs/decisions/README.md 可以直接创建或更新。

4. 禁止修改：

   * src/main/java
   * src/test/java
   * src/main/resources
   * pom.xml
   * README.md
   * mvnw
   * mvnw.cmd
   * 任何业务代码
   * 任何测试代码
   * 任何构建配置

5. 文档内容必须基于项目事实。
   不确定的信息写“未确认”。
   不要脑补。
   不要提前设计未来功能。
   不要写 GET /api/owners/{ownerId}/pets。
   不要写 DELETE /api/pets/{petId} 修改方案。

6. 文件内容要求：

   product.md：

   * 项目目标
   * 业务领域
   * 核心实体
   * 当前功能边界
   * 明确非目标

   tech.md：

   * Java / Spring Boot / Maven 版本
   * 数据库
   * 测试框架
   * API 文档方式
   * 运行方式
   * 禁止随意引入的新技术

   structure.md：

   * 目录结构
   * 主要 package
   * Controller / Service / Repository / Model / DTO 的组织方式
   * 测试目录结构
   * 后续新增代码应该放在哪里

   AGENTS.md：

   * 先读 steering 文档
   * 每次只做一个 task
   * 不扩大需求
   * 不新增依赖，除非明确允许
   * 不修改未授权文件
   * 不执行 git add
   * 不执行 git commit
   * 完成后报告修改文件、测试结果、git diff --stat

   docs/lessons/README.md：

   * 说明这里用于记录 AI 错误、工具坑、流程教训
   * 不要虚构已有教训

   docs/decisions/README.md：

   * 说明这里用于记录长期架构决策和技术取舍
   * 不要虚构已有决策

7. 完成后只输出：

   * 创建/修改的文件列表
   * 是否只改了允许文件
   * git diff --stat
   * 未确认问题

不要输出长篇解释。
完成后停止。
```
