# 配置 H2 和 JPA

让 Spring Boot 启动时自动创建日志表。

本课使用：

```text
ddl-auto: update
```

意思是根据 Entity 自动更新表结构。学习阶段可以用，生产环境要用 Flyway / Liquibase 管理数据库变更。

#### 代码

修改 `application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:ai_gateway
    driver-class-name: org.h2.Driver
    username: sa
    password:

  h2:
    # H2 控制台地址：http://localhost:8080/h2-console
    console:
      enabled: true
      path: /h2-console

  jpa:
    hibernate:
      ddl-auto: update
    show-sql: false
```
