# 添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

# 配置连接信息

```yaml
spring:
  redis:
      host: 127.0.0.1 
      port: 6379
      password: 123456
      jedis:
        pool:
          max-active: 8
          max-wait: -1
          max-idle: 500
          min-idle: 0
      lettuce:
        shutdown-timeout: 0
```

# 测试

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test_1{
    @Autowired
    private RedisTemplate<String,String> redisTemplate;

    @Test
    public void set(){
        redisTemplate.opsForValue().set("myKey","myValue");
        System.out.println(redisTemplate.opsForValue().get("myKey"));
    }
}
```

# 配置序列化器将实体类以JSON的形式储存到Redis中

entity要实现Serializable接口

设置序列化器
```java
@Configuration
public class RedisConfig{
    @Bean
    public RedisTemplate<String, MyObj> redisTemplate(RedisConnectionFactory factory){
        RedisTemplate<String,MyObj> template = new RedisTemplate<>();
        //关联
        template.setConnectionFactory(factory);
        //设置key的序列化器
        template.setKeySerializer(new StringRedisSerializer());
        //设置value的序列化器
        template.setValueSerializer(new Jackson2JsonRedisSerializer<>(MyObj.class));
        return template;
    }
}
```

测试
```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class RedisTest {

    @Autowired
    private RedisTemplate<String,Days> redisTemplate;
    private MyObj d;
    @Before
    public void before(){
        d=new MyObj();
        d.setTitle("title");
    }
    @Test
    public void testSet(){
        this.redisTemplate.opsForValue().set("days", d);
        System.out.println((redisTemplate.opsForValue().get("days")));
    }
}
```
