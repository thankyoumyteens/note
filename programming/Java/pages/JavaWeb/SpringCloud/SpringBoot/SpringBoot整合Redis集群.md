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
    pool:
      max-active: 1000  # 连接池最大连接数(使用负值表示没有限制)
      max-idle: 10    # 连接池中的最大空闲连接
      max-wait: -1   # 连接池最大阻塞等待时间(使用负值表示没有限制)
      min-idle: 5     # 连接池中的最小空闲连接
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
