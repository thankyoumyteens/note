# 多数据源

1. 依赖

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>dynamic-datasource-spring-boot3-starter</artifactId>
    <version>4.3.1</version>
</dependency>
```

2. 数据源配置

```yaml
spring:
  datasource:
    dynamic:
      # 启用动态数据源, 默认true
      enabled: true
      # 设置默认的数据源或者数据源组,默认master
      primary: mysql01
      # 严格匹配数据源,默认false. true未匹配到指定数据源时抛异常,false使用默认数据源
      strict: false
      # 是否优雅关闭数据源, 默认false, 设置为true时, 关闭数据源时如果数据源中还存在活跃连接, 至多等待10s后强制关闭
      grace-destroy: false
      datasource:
        # 数据源1
        mysql01:
          url: jdbc:mysql://127.0.0.1:3306/dynamic
          username: root
          password: 123456
          driver-class-name: com.mysql.cj.jdbc.Driver
        # 数据源2
        mysql02:
          url: jdbc:mysql://127.0.0.1:3307/dynamic
          username: root
          password: 123456
          driver-class-name: com.mysql.cj.jdbc.Driver
        # 数据源3
        oracle01:
        # 省略...
```

3. 数据源 oracle01 的 mapper

```java
// @DS可以注解在方法上或类上, 同时存在的话, 方法上的注解优先于类上的注解
// 没有@DS时, 使用默认数据源
@DS("oracle01")
public public interface WordsMapper extends BaseMapper<Words> {
}
```

4. 数据源 mysql01 的 mapper

```java
@DS("mysql01")
public interface BookMapper extends BaseMapper<Book> {
}
```

5. 使用不同的 mapper

```java
@Component
public class ConsoleApp implements CommandLineRunner {
    @Autowired
    private WordsMapper wordsMapper;
    @Autowired
    private BookMapper bookMapper;

    @Override
    public void run(String... args) throws Exception {
        List<Words> words = wordsMapper.selectList(Wrappers.<Words>query());
        System.out.println(words);
        System.out.println("--------------------------------------------------");
        List<Book> books = bookMapper.selectList(Wrappers.<Book>query());
        System.out.println(books);
    }
}
```

## @DS 注解失效的情况

1. 开启了 spring 的事务, 调用不同数据源的方法上不能加 @Transactional 注解
