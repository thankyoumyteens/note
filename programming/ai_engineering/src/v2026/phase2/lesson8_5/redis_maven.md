# 添加 Redis 依赖

`spring-boot-starter-data-redis` 会提供 Redis 客户端相关能力。我们本课不深入 Redis 客户端底层，只需要知道：后面 `RedisRateLimiter` 会用 `StringRedisTemplate` 操作 Redis。

#### 代码

修改 `pom.xml`，加入：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

这会让项目具备：

```text
Redis 连接能力
StringRedisTemplate
Redis Lua Script 执行能力
```
