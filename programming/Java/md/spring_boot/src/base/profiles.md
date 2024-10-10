# 多环境配置

## 2.4 版本之前

application.yml:

```yaml
# 开发环境
spring:
  profiles: dev
server:
  port: 80

# 在 application.yml 中使用 --- 来分割不同的配置
---
# 测试环境
spring:
  profiles: test
server:
  port: 82
```

## 2.4 版本之后

1. 公用配置 application.yml:

```yaml
server:
  port: 8000
```

2. 开发环境配置 application-dev.yml:

```yaml
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:sqlite:/home/demo/Downloads/demo.db
    driver-class-name: org.sqlite.JDBC
```

3. 线上环境配置 application-release.yml

```yaml
spring:
  config:
    activate:
      on-profile: release
  datasource:
    url: jdbc:sqlite:/demo/db/demo.db
    username: demo
    password: 123456
    driver-class-name: org.sqlite.JDBC
```

## 使用

通过 JVM 参数设置环境:

```sh
java -Dspring.profiles.active=test -jar demo.jar
```

通过参数设置环境:

```sh
java –jar demo.jar –-spring.profiles.active=test
```
