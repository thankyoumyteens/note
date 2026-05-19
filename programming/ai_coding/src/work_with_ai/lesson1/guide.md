# 如果 AI 过度设计，怎么纠正

如果它加入了数据库、Security、Docker、Spring AI 等内容，发这个纠正 Prompt：

```text
当前实现过度设计。目前只允许创建最小可运行 Spring Boot 项目骨架。

请移除或不要加入以下内容：
1. 数据库相关依赖和配置
2. Spring Security
3. Docker / docker-compose
4. 前端
5. 真实 AI API
6. Spring AI
7. 用户系统
8. 复杂业务模块
9. 不必要依赖

请保留：
1. pom.xml
2. Spring Boot 主启动类
3. GET /api/health
4. 基础测试
5. README.md

目标是让 mvn test 通过，并保持项目结构尽量简单。
```
