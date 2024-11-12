# 连接数据库

## mariadb

1. 依赖

```xml
<dependency>
    <groupId>org.mariadb.jdbc</groupId>
    <artifactId>mariadb-java-client</artifactId>
    <version>3.5.0</version>
</dependency>
```

2. 配置

```yaml
spring:
  datasource:
    url: jdbc:mariadb://127.0.0.1:3306/test_db?characterEncoding=UTF-8&useSSL=false
    username: root
    password: 123456
    driver-class-name: org.mariadb.jdbc.Driver
```

## mysql

1. 依赖

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

2. 配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/test_db?characterEncoding=UTF-8&useSSL=false
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
```

## oracle

1. 依赖

```xml
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ojdbc6</artifactId>
    <version>11.2.0.4</version>
</dependency>
```

2. 配置

```yaml
spring:
  datasource:
    url: jdbc:oracle:thin:@127.0.0.1:1521/orcl
    username: TEST01
    password: 123456
    driver-class-name: oracle.jdbc.OracleDriver
```

## sqlite

1. 依赖

```xml
<dependency>
    <groupId>org.xerial</groupId>
    <artifactId>sqlite-jdbc</artifactId>
    <version>3.46.1.3</version>
</dependency>
```

2. 配置

```yaml
spring:
  datasource:
    url: jdbc:sqlite:/home/test.db
    driver-class-name: org.sqlite.JDBC
```
