# 推荐 Prompt

你可以在空目录中使用 Codex 或 Claude Code。

先创建目录：

```bash
mkdir ai-doc-summary
cd ai-doc-summary
```

然后把下面这段发给 Codex / Claude Code：

```text
目标：
从空目录创建一个最小可运行的 Java 21 + Spring Boot 3.x + Maven 项目，项目名为 ai-doc-summary。

背景：
这是 AI 工具驱动开发工作流课程的实战项目。当前目录为空，没有任何已有代码。项目后续会逐步实现文档保存、文档查询、摘要模拟、测试、Spec Workflow、MCP、Skills、Commands、Hooks、Code Review 和 Handoff 等工作流能力。

输入：
当前只有空目录。你可以创建 Maven 项目结构和必要文件。

输出：
请创建最小可运行项目，包括：
1. pom.xml
2. Spring Boot 主启动类
3. 一个健康检查接口 GET /api/health
4. 一个基础测试
5. README.md，写明测试和启动命令

限制：
1. 不要加入数据库。
2. 不要加入 Spring Security。
3. 不要加入 Docker。
4. 不要加入前端。
5. 不要接入真实 AI API。
6. 不要加入 Spring AI。
7. 不要加入用户系统。
8. 不要加入复杂分层。
9. 不要引入不必要依赖。
10. 不要生成复杂业务功能，本课只要最小项目骨架。

验收标准：
1. mvn test 可以通过。
2. mvn spring-boot:run 可以启动。
3. GET /api/health 返回 OK 或类似健康状态。
4. 项目结构清晰，文件数量尽量少。
5. README.md 包含测试命令和启动命令。
6. 没有数据库、Security、Docker、前端、真实 AI API、Spring AI 或用户系统。
7. 运行 mvn spring-boot:run 验证项目启动后，请不要长期占用 8080。如果需要启动服务，请在验证完成后停止进程。不要把 Spring Boot 进程留在后台。
8. 完成后请总结创建了哪些文件、如何测试、如何启动、如何访问健康检查接口。
```
