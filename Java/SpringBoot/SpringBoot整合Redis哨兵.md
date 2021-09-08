# 添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

# application.yml

```yaml
spring:
  redis:
    password: passw0rd
    timeout: 5000
    sentinel:
      # master的别名
      master: mymaster
      # 多个哨兵用逗号分隔
      nodes: 192.168.40.201:26379,192.168.40.201:36379,192.168.40.201:46379
    jedis:
      pool:
        max-active: 8
        max-wait: -1
        max-idle: 8
        min-idle: 0
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
