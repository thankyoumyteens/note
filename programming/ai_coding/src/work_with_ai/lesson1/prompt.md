# 推荐你实际发给 Codex / Claude Code 的 Prompt

## Codex 版本

在你准备好的空目录中执行：

```bash
mkdir ai-doc-summary
cd ai-doc-summary
git init
```

然后运行 Codex 输入以下内容：

```text
目标：
从空目录创建一个最小可运行的 Java 21 + Spring Boot 3.x + Maven 项目，项目名为 ai-doc-summary。

背景：
这是 AI 工作指挥方法课程的实战项目。当前目录为空，没有任何已有代码。项目后续会逐步实现文档保存、AI 摘要生成、摘要查询等功能。

输入：
当前只有空目录。你可以创建 Maven 项目结构和必要文件。

输出：
请创建最小可运行项目，包括：
1. pom.xml
2. 主启动类
3. 一个健康检查接口 GET /api/health
4. 一个基础测试
5. README.md 中写明启动和测试命令

限制：
1. 不要加入数据库。
2. 不要加入 Spring Security。
3. 不要加入 Docker。
4. 不要加入前端。
5. 不要接入真实 AI API。
6. 不要生成复杂分层，只保留最小结构。

验收标准：
1. mvn test 可以通过。
2. mvn spring-boot:run 可以启动。
3. GET /api/health 返回 OK 或类似健康状态。
4. 项目结构清晰，文件数量尽量少。
5. README.md 包含运行方式。

完成后请总结：
1. 创建了哪些文件
2. 如何运行测试
3. 如何启动项目
4. 如何访问健康检查接口
```

---

## Claude Code 版本

在空目录中打开 Claude Code，然后输入：

```text
目标：
从空目录创建一个最小可运行的 Java 21 + Spring Boot 3.x + Maven 项目，项目名为 ai-doc-summary。

背景：
这是 AI 工作指挥方法课程的实战项目。当前目录为空，没有任何已有代码。项目后续会逐步实现文档保存、AI 摘要生成、摘要查询等功能。

输入：
当前只有空目录。你可以创建 Maven 项目结构和必要文件。

输出：
请创建最小可运行项目，包括：
1. pom.xml
2. 主启动类
3. 一个健康检查接口 GET /api/health
4. 一个基础测试
5. README.md 中写明启动和测试命令

限制：
1. 不要加入数据库。
2. 不要加入 Spring Security。
3. 不要加入 Docker。
4. 不要加入前端。
5. 不要接入真实 AI API。
6. 不要生成复杂分层，只保留最小结构。

验收标准：
1. mvn test 可以通过。
2. mvn spring-boot:run 可以启动。
3. GET /api/health 返回 OK 或类似健康状态。
4. 项目结构清晰，文件数量尽量少。
5. README.md 包含运行方式。

完成后请总结：
1. 创建了哪些文件
2. 如何运行测试
3. 如何启动项目
4. 如何访问健康检查接口
```
