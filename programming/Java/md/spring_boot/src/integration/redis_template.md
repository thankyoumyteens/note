# 集成 Redis

### 1. 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

### 2. 配置 Redis 连接信息

```yaml
spring:
  redis:
    host: 127.0.0.1
    port: 6379
```

### 3. 创建 RedisTemplate

```java
package com.example;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;

@Configuration
public class RedisConfig {

  @Bean
  public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
    RedisTemplate<String, Object> template = new RedisTemplate<>();
    template.setConnectionFactory(connectionFactory);
    // 序列化key
    template.setKeySerializer(new StringRedisSerializer());
    // 序列化value
    template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
    return template;
  }
}
```

### 4. 使用 RedisTemplate

```java
package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class ConsoleApp implements CommandLineRunner {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public void run(String... args) throws Exception {
        // 设置键值对
        redisTemplate.opsForValue().set("name", "zhangsan");

        // 获取值
        String value = (String) redisTemplate.opsForValue().get("name");
    }
}
```

## 注意

```java
public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
    ...
}
```

和

```java
@Autowired
private RedisTemplate<String, Object> redisTemplate;
```

的泛型必须保持一致, 否则会无法注入!
