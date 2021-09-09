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
    password: 123456
    cluster:
      nodes: 192.168.0.203:7000,192.168.0.203:7001,192.168.0.203:7002
      max-redirects: 3
    lettuce:
      pool:
        max-idle: 16
        max-active: 32
        min-idle: 8
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
