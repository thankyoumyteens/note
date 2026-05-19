# 你要检查 AI 的输出

完成后检查项目结构，理想结果大概是：

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
```

也可能没有单独的 `HealthController.java`，而是放在主类旁边。只要结构清晰、能跑、不过度设计即可。

## 检查依赖是否过度

第 1 课合理依赖通常只有：

```text
spring-boot-starter-web
spring-boot-starter-test
```

不应该出现：

```text
spring-boot-starter-data-jpa
spring-boot-starter-security
spring-ai
postgresql
mysql
redis
jjwt
openapi
docker
lombok
```

`lombok` 也不建议第 1 课加入，因为现在没有复杂模型。

## 运行验收命令

项目生成后，运行：

```bash
mvn test
```

通过后启动项目：

```bash
mvn spring-boot:run
```

再开一个终端访问：

```bash
curl http://localhost:8080/api/health
```

预期返回类似：

```text
OK
```

或者：

```json
{
  "status": "OK"
}
```

两种都可以。
