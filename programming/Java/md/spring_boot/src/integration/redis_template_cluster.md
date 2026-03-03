# 集成RedisCluster

### 1. 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

### 2. 配置 Redis 连接信息(application.yml)

Spring Boot 能够自动识别 cluster 配置。即使你本地有 6 个节点，通常只需列出其中几个，程序启动时会自动通过 CLUSTER NODES 命令发现整个集群的拓扑结构。

```yaml
spring:
  data:
    redis:
      cluster:
        nodes:
          - 127.0.0.1:30001
          - 127.0.0.1:30002
          - 127.0.0.1:30003
          - 127.0.0.1:30004
          - 127.0.0.1:30005
          - 127.0.0.1:30006
        max-redirects: 3 # 最大重定向次数
      lettuce:
        cluster:
          refresh:
            adaptive: true # 开启自适应拓扑刷新（当集群扩缩容时自动感知）
            period: 60s # 定时刷新周期
      password: "" # 如果没有设置密码，留空即可
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
