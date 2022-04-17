application.yml
```yaml
spring:
  redis:
    cluster:
      nodes: 192.168.1.101:8001,192.168.1.101:8002,192.168.1.102:8001,192.168.1.102:8002,192.168.1.103:8001,192.168.1.103:8002
      max-redirects: 3
    pool:
      max-active: 1000  # 连接池最大连接数（使用负值表示没有限制）
      max-idle: 10    # 连接池中的最大空闲连接
      max-wait: -1   # 连接池最大阻塞等待时间（使用负值表示没有限制）
      min-idle: 5     # 连接池中的最小空闲连接
    timeout: 6000  # 连接超时时长（毫秒）
    password: FC7EF9622A3D2B62 #redis加密密码
```

自定义 RedisConnectionFactory
```java
@Configuration
public class RedisConfig {
 
    private final Environment environment;
    public RedisConfig(Environment environment) {
        this.environment = environment;
    }
 
    @Bean(name = "myredisConnectionFactory")
    public RedisConnectionFactory myLettuceConnectionFactory() {
        Map<String, Object> source = new HashMap<String, Object>();
        source.put("spring.redis.cluster.nodes", environment.getProperty("spring.redis.cluster.nodes"));
        source.put("spring.redis.cluster.timeout", environment.getProperty("spring.redis.cluster.timeout"));
        source.put("spring.redis.cluster.max-redirects", environment.getProperty("spring.redis.cluster.max-redirects"));
        MapPropertySource mapPropertySource = new MapPropertySource("RedisClusterConfiguration", source);
        RedisClusterConfiguration  redisClusterConfiguration = new RedisClusterConfiguration(mapPropertySource);
 
        //获取application.yml 中的密码（密文）
        String password = environment.getProperty("spring.redis.password");
        //解密密码并添加到配置中
        redisClusterConfiguration.setPassword(DesUtils.decode(password));
        return new LettuceConnectionFactory(redisClusterConfiguration);
    }
 
    @Bean
    public RedisTemplate<String, Serializable> redisTemplate(@Qualifier("myredisConnectionFactory") RedisConnectionFactory factory) {
        RedisTemplate<String, Serializable> template = new RedisTemplate<>();
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setConnectionFactory(factory);
        return template;
    }
 
    @Bean
    public StringRedisTemplate createStringRedisTemplate(@Qualifier("myredisConnectionFactory") RedisConnectionFactory factory){
        StringRedisTemplate stringRedisTemplate = new StringRedisTemplate(factory);
        stringRedisTemplate.setKeySerializer(new StringRedisSerializer());
        stringRedisTemplate.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        return stringRedisTemplate;
    }
}
```

使用
```java
@Autowired
private RedisTemplate redisTemplate;

@Autowired
private StringRedisTemplate stringRedisTemplate;

public void test(){
    stringRedisTemplate.boundValueOps("name").set("wuchao", 500, TimeUnit.SECONDS);
    String name = stringRedisTemplate.boundValueOps("name").get();
    System.out.println(name);
}
```
