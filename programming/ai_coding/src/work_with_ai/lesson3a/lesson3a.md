# 第 3A 课：项目启动流程工具化

第 1～3 课你已经完成了：

```text
第 1 课：从空目录创建最小 Spring Boot 项目
第 2 课：建立 AGENTS.md / CLAUDE.md
第 3 课：建立 .gitignore 和 Git baseline
```

第 3A 课不是继续写业务代码，而是把这三课总结成一个可复用流程：

```text
以后我新建一个 Java + AI coding tools 项目时，应该怎么启动？
```

最终产物是：

```text
WORKFLOW.md 初版
```

它的作用是：把一次性的对话经验沉淀成项目级工作流文档。

## 为什么要做第 3A 课

如果没有 `WORKFLOW.md`，你以后每次新项目都要重新想：

```text
要不要让 AI 直接生成项目？
要不要用 Spring Initializr？
AGENTS.md / CLAUDE.md 什么时候建？
.gitignore 什么时候建？
什么时候 git commit？
什么时候运行 mvn test？
Claude Code 启动服务后怎么处理 8080？
```

`WORKFLOW.md` 的价值是：

> 把“启动项目的步骤”标准化，让下一个项目可以直接复用。

## 本课要比较的三种项目启动方式

### 方式 1：让 AI 从空目录生成项目

优点：

```text
适合学习和原型
能训练你如何描述清晰任务
AI 可以同时生成 README、测试和健康检查接口
```

缺点：

```text
可能过度设计
可能生成不稳定的 pom.xml
可能引入无关依赖
需要你严格限制范围
```

适用场景：

```text
课程练习
小型原型
你想练习 AI 指挥能力
```

---

### 方式 2：使用 Spring Initializr 生成项目

优点：

```text
官方脚手架更稳定
pom.xml 更规范
依赖版本更可靠
适合正式项目起步
```

缺点：

```text
不会自动生成你的 AGENTS.md / CLAUDE.md
不会自动生成项目工作流规则
仍然需要 AI 帮你补规则、README、测试和 baseline
```

适用场景：

```text
正式 Java 项目
你更关心基础工程稳定性
你不想让 AI 猜 Spring Boot 初始化细节
```

---

### 方式 3：使用 Maven Wrapper 固化构建工具

Maven Wrapper 产物一般包括：

```text
mvnw
mvnw.cmd
.mvn/wrapper/...
```

价值是：

```text
团队成员不必自己安装完全相同版本的 Maven
CI 或新机器上更容易复现构建
项目构建方式更稳定
```

但第 3A 课只需要理解和记录，不一定马上引入。因为这属于项目启动工具化，不是业务功能。
