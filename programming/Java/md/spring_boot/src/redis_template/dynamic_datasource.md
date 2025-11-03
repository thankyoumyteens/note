# 多数据源

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
    myredis1:
      host: 127.0.0.1
      port: 6379
    myredis2:
      host: 127.0.0.1
      port: 6380
```

### 3. 创建 RedisTemplate

```java
package com.example;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceClientConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;

import java.time.Duration;

@Configuration
public class RedisConfiguration {

    @Value("${spring.redis.myredis1.host}")
    private String redis1Host;

    @Value("${spring.redis.myredis1.port}")
    private int redis1Port;

    @Value("${spring.redis.myredis2.host}")
    private String redis2Host;

    @Value("${spring.redis.myredis2.port}")
    private int redis2Port;

    /**
     * 创建 Redis 连接工厂
     *
     * @param host Redis 主机地址
     * @param port Redis 端口号
     * @return Redis 连接工厂
     */
    public JedisConnectionFactory redisConnectionFactory(String host, int port) {
        // 配置 Redis 单机服务器信息
        RedisStandaloneConfiguration config = new RedisStandaloneConfiguration();
        config.setHostName("localhost");
        config.setPort(6380);
        config.setPassword(RedisPassword.of("123456"));
        config.setDatabase(0);

        // 创建连接工厂
        JedisConnectionFactory factory = new JedisConnectionFactory(config);
        // 关键：手动触发初始化(Spring 自动配置会自动调用，这里是手动创建, 所以需显式调用)
        factory.afterPropertiesSet();
        return factory;
    }

    @Bean(name = "redisTemplate1")
    public RedisTemplate<String, Object> redisTemplate1() {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        // 设置连接工厂
        template.setConnectionFactory(redisConnectionFactory(redis1Host, redis1Port));
        return template;
    }

    @Bean(name = "redisTemplate2")
    public RedisTemplate<String, Object> redisTemplate2() {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        // 设置连接工厂
        template.setConnectionFactory(redisConnectionFactory(redis2Host, redis2Port));
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
    private RedisTemplate<String, Object> redisTemplate1;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate2;

    @Override
    public void run(String... args) throws Exception {
        redisTemplate1.opsForValue().set("key1", "value1");
        System.out.println(redisTemplate1.opsForValue().get("key1"));

        redisTemplate2.opsForValue().set("key2", "value2");
        System.out.println(redisTemplate2.opsForValue().get("key2"));
    }
}
```
