# 集群模式

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisPassword;
import org.springframework.data.redis.connection.RedisClusterConfiguration;
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
        // 配置 Redis 服务器信息（集群模式）
        // 配置集群节点（至少填 1 个节点，会自动发现集群其他节点）
        RedisClusterConfiguration redisConfig = new RedisClusterConfiguration();
        redisConfig.addClusterNode(new RedisNode("cluster-node1", 6379));
        redisConfig.addClusterNode(new RedisNode("cluster-node2", 6380));
        redisConfig.addClusterNode(new RedisNode("cluster-node3", 6381));

        // 配置集群参数
        redisConfig.setMaxRedirects(5); // 最大重定向次数（默认 5）
        redisConfig.setPassword(RedisPassword.of("cluster-password")); // 集群统一密码

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
