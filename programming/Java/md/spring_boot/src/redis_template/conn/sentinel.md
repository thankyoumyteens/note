# 哨兵模式

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisPassword;
import org.springframework.data.redis.connection.RedisSentinelConfiguration;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import redis.clients.jedis.JedisPoolConfig;

@Configuration
public class RedisConfig {

    // 配置 Jedis 连接池参数
    @Bean
    public JedisPoolConfig jedisPoolConfig() {
        JedisPoolConfig poolConfig = new JedisPoolConfig();

        // 最大总连接数：根据业务场景调整，不宜过大（避免资源耗尽）
        poolConfig.setMaxTotal(200);
        // 最大空闲连接数：保持一定的空闲连接，减少创建连接的开销
        poolConfig.setMaxIdle(50);
        // 最小空闲连接数：确保有足够的基础连接可用
        poolConfig.setMinIdle(20);
        // 最大等待时间：当无可用连接时，最多等待 3 秒（超时则抛出异常）
        poolConfig.setMaxWaitMillis(3000);
        // 借出连接时测试有效性：避免使用已断开的连接
        poolConfig.setTestOnBorrow(true);
        // 空闲时测试连接有效性：定期清理无效连接
        poolConfig.setTestWhileIdle(true);
        // 空闲连接检测间隔（毫秒）：每 5 秒检测一次
        poolConfig.setTimeBetweenEvictionRunsMillis(5000);
        // 连接最小空闲时间（毫秒）：超过 30 秒空闲的连接可能被移除
        poolConfig.setMinEvictableIdleTimeMillis(30000);

        return poolConfig;
    }

    // 配置 Jedis 连接工厂（结合连接池和 Redis 服务器信息）
    @Bean
    public JedisConnectionFactory jedisConnectionFactory(JedisPoolConfig poolConfig) {
        // 配置 Redis 服务器信息（哨兵模式）
        RedisSentinelConfiguration redisConfig = new RedisSentinelConfiguration()
                .master("mymaster"); // 哨兵监控的主节点名称

        // 添加哨兵节点列表（至少配置 1 个，会自动发现其他哨兵）
        redisConfig.addSentinel(new RedisNode("sentinel-1", 26379));
        redisConfig.addSentinel(new RedisNode("sentinel-2", 26379));
        redisConfig.addSentinel(new RedisNode("sentinel-3", 26379));

        // 配置 Redis 主从节点密码（若有）
        redisConfig.setPassword(RedisPassword.of("redis-password"));
        // 若哨兵节点本身需要密码认证
        redisConfig.setSentinelPassword(RedisPassword.of("sentinel-password"));

        // 创建连接工厂，并关联连接池配置
        JedisConnectionFactory factory = new JedisConnectionFactory(redisConfig);
        factory.setPoolConfig(poolConfig); // 绑定连接池配置

        // 初始化连接工厂（可选，若不调用则首次使用时自动初始化）
        factory.afterPropertiesSet();

        return factory;
    }

    // 配置 RedisTemplate（基于连接工厂）
    @Bean
    public RedisTemplate<String, Object> redisTemplate(JedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);

        // 配置序列化器（示例：key 用 String 序列化，value 用 JSON 序列化）
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());

        template.afterPropertiesSet();
        return template;
    }
}
```
