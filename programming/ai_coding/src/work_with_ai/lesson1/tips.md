# 本课你要特别观察 AI 的行为

当你把上面的 prompt 发给 Codex 或 Claude Code 后，不是只看它有没有生成代码。

你要检查 5 件事。

## 检查 1：有没有过度设计

不应该出现：

```text
Spring Security
JWT
UserController
数据库配置
Dockerfile
docker-compose.yml
Redis
PostgreSQL
前端目录
复杂异常体系
复杂领域模型
```

如果出现，说明限制没有被遵守。

---

## 检查 2：项目结构是否足够简单

理想结构大概是这样：

```text
ai-doc-summary/
  pom.xml
  README.md
  src/
    main/
      java/
        com/example/aidocsummary/
          AiDocSummaryApplication.java
          HealthController.java
    test/
      java/
        com/example/aidocsummary/
          AiDocSummaryApplicationTests.java
          HealthControllerTest.java
```

可以略有不同，但第一版不应该太复杂。

---

## 检查 3：pom.xml 是否干净

第一版依赖一般只需要：

```text
spring-boot-starter-web
spring-boot-starter-test
```

可以有：

```text
spring-boot-maven-plugin
```

不应该一开始就有：

```text
spring-boot-starter-data-jpa
spring-boot-starter-security
postgresql
mysql
redis
lombok
openapi
jjwt
```

尤其是 `lombok`，第 1 课不需要。

---

## 检查 4：健康检查接口是否简单

可以是：

```java
@GetMapping("/api/health")
public String health() {
    return "OK";
}
```

或者返回 JSON：

```json
{
  "status": "OK"
}
```

两者都可以。第 1 课不需要复杂健康指标。

---

## 检查 5：测试是否真的能跑

你要自己运行：

```bash
mvn test
```

如果通过，再启动：

```bash
mvn spring-boot:run
```

然后访问：

```bash
curl http://localhost:8080/api/health
```

如果返回 `OK` 或类似健康状态，第 1 课的项目骨架就成功了。
