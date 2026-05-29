# 添加数据库依赖

本课不引入复杂 ORM。RAG 检索需要写向量 SQL，`JdbcTemplate` 更直接。

#### 代码

`pom.xml` 添加：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

#### 删除 H2 依赖

现在已经进入 RAG 阶段，可以把 H2 删除，统一切到 PostgreSQL ，这样后续 RAG、日志持久化、权限隔离、Text-to-SQL 都更一致。

在 pom.xml 里删除类似这一段：

```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```
