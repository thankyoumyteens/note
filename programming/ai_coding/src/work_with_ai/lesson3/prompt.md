# 本课推荐 Prompt

```text
目标：
检查当前 ai-doc-summary 项目是否适合作为初始 Git baseline，并补齐必要的 .gitignore。

背景：
当前项目已经完成：
1. 第 1 课：从空目录创建最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：创建 AGENTS.md 和 CLAUDE.md 项目规则文件。
现在要进行第 3 课：初始化 Git 与基线提交。

输入：
请查看当前项目结构、pom.xml、README.md、AGENTS.md、CLAUDE.md、src/ 和当前 Git 状态。

输出：
请先检查并输出：
1. 当前项目结构摘要
2. 当前 git status 摘要
3. 是否存在明显不应提交的文件
4. 是否存在或需要新增 .gitignore
5. 推荐的 .gitignore 内容
6. 建议的首次提交信息

执行要求：
1. 如果 .gitignore 不存在，请创建一个适合 Java + Maven + IntelliJ/VS Code 的最小 .gitignore。
2. 如果 .gitignore 已存在，请只做必要补充。
3. 不要修改 pom.xml。
4. 不要修改 Java 源码。
5. 不要修改测试代码。
6. 不要修改 README.md。
7. 不要修改 AGENTS.md 或 CLAUDE.md。
8. 不要新增依赖。
9. 不要执行 git add。
10. 不要执行 git commit。
11. 不要运行 mvn spring-boot:run。
12. 如果需要验证，只运行 mvn test。
13. 完成后运行 git status，并总结下一步我应该手动执行的命令。

限制：
1. 不要删除任何源码文件。
2. 不要引入数据库、Security、Docker、前端、真实 AI API 或 Spring AI。
3. 不要创建复杂脚本。
4. 不要提交 target/、.idea/、.vscode/、*.log、*.class 等本地文件或构建产物。
5. 不要让任何 Java 进程长期占用 8080。

验收标准：
1. 根目录存在 .gitignore。
2. .gitignore 至少排除 target/、.idea/、.vscode/、*.log、*.class、.DS_Store。
3. git status 中不应出现 target/ 作为待提交文件。
4. mvn test 可以通过。
5. Claude Code 不应自动执行 git add 或 git commit。
6. 完成后给出建议的手动提交命令和 commit message。
```
