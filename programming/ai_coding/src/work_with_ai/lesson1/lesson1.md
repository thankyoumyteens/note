# 第 1 课：把“我要一个 Java 项目”变成清晰任务

本课不是直接写代码，而是训练你如何把一句模糊需求：

```text
帮我创建一个 Java 后端项目。
```

改写成 AI coding agent 可以稳定执行的任务。

最终你要能让 Codex / Claude Code 从空目录创建一个：

```text
最小可运行
可测试
不复杂化
后续可扩展
```

的 Spring Boot 项目。

# 为什么不能直接说“帮我创建一个 Java 项目”

因为从零项目最容易被 AI 过度发挥。

如果你只说：

```text
帮我创建一个 Java Spring Boot 项目。
```

AI 可能会自动加上：

```text
数据库
Spring Security
Docker
Redis
Swagger
前端
复杂分层
真实 AI API
用户系统
权限系统
```

但这些都不是第 1 课要做的事情。

第 1 课只需要：

```text
pom.xml
Spring Boot 主启动类
健康检查接口
基础测试
README.md
```

也就是一个最小项目骨架。
