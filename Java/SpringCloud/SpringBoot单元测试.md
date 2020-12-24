# SpringBoot2 + Junit5

依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
    <exclusions>
        <exclusion>
            <groupId>org.junit.vintage</groupId>
            <artifactId>junit-vintage-engine</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

测试类
```java
@SpringBootTest
class DemoApplicationTests {

    @Autowired
    private WebApplicationContext webApplicationContext;

    @Test
    void contextLoads() {
    }
}
```

# SpringBoot2 + Junit4

依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

测试类
```java
@RunWith(SpringRunner.class)
@SpringBootTest
class DemoApplicationTests {

    @Autowired
    private WebApplicationContext webApplicationContext;

    @Test
    void contextLoads() {
    }
}
```
