# 添加 JPA 和数据库依赖

本课用 JPA 是为了快速完成“持久化日志”能力。生产环境可以换成 MySQL、PostgreSQL、ClickHouse、Elasticsearch 或日志平台。

为了本地学习简单，先用 H2 数据库。

#### 代码

修改 `pom.xml`，新增：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```
