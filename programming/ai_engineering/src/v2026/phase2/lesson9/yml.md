# 确认 Spring Boot / Spring AI 版本边界

避免一上来就因为 Spring AI 版本和 Spring Boot 版本不匹配导致依赖拉不下来或启动失败。

Spring AI 版本和 Spring Boot 版本有关。官方文档显示 Spring AI 支持 Spring Boot 3.4.x 和 3.5.x；[Spring AI GitHub README](https://github.com/spring-projects/spring-ai) 也说明 Spring AI 1.1.x 对应 Spring Boot 3.5.x，Spring AI 2.x 对应 Spring Boot 4.x。

当前课程建议：

```text
如果你的项目是 Spring Boot 3.5.x：
使用 Spring AI 1.1.0

如果你的项目是 Spring Boot 4.x：
再考虑 Spring AI 2.x
```

本课按 Spring Boot 3.5.x / Spring AI 1.1.0 设计。Spring AI 1.0.0 以后已经在 Maven Central，不需要再配置 Spring milestone 仓库。

#### 代码

先检查 `pom.xml` 里的 Spring Boot 版本：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.x</version>
</parent>
```

如果你是 `3.4.x`，也可以继续尝试 Spring AI 1.1.0；如果依赖冲突，再降到 Spring AI 1.0.x。

不要直接用 Spring AI 2.x，除非你的 Spring Boot 已经升级到 4.x。
