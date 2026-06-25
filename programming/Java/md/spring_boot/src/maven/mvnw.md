# mvnw

`mvnw` 是 **Maven Wrapper** 的启动脚本。

它的作用是：**让项目自己携带 Maven 版本管理能力，而不是要求你电脑上提前安装 Maven。**

在 Java / Spring Boot 项目里你经常会看到这些文件：

```text
mvnw
mvnw.cmd
.mvn/wrapper/
```

含义是：

```text
mvnw        macOS / Linux 用
mvnw.cmd    Windows 用
.mvn/        Maven Wrapper 配置目录
```

平时如果你看到教程写：

```bash
./mvnw test
./mvnw spring-boot:run
./mvnw clean package
```

意思就是用项目自带的 Maven Wrapper 来执行 Maven 命令。

它和直接用 `mvn` 的区别：

```text
mvn   = 使用你电脑全局安装的 Maven
mvnw  = 使用项目指定的 Maven 版本
```

所以工程实践里更推荐用 `mvnw`，因为团队里每个人、CI 环境、AI coding 工具都能使用同一个 Maven 版本，减少“我这里能跑，你那里不能跑”的问题。

如果项目里有 `mvnw`，优先用它。
