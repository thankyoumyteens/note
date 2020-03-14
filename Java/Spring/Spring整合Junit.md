# 引入依赖
```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-test</artifactId>
  <version>5.0.2.RELEASE</version>
</dependency>
```

# 使用@RunWith 注解替换原有运行器
```java
@RunWith(SpringJUnit4ClassRunner.class)
public class AccountServiceTest {}
```

# 使用@ContextConfiguration 指定 spring 配置文件的位置
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations= {"classpath:bean.xml"})
public class AccountServiceTest {}
```

# 使用@Autowired 注入数据
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations= {"classpath:bean.xml"})
public class AccountServiceTest {
  @Autowired
  private IAccountService as = null;

  @Test
  public void testFindAll() {
    List<Account> accounts = as.findAllAccount();
    for(Account account : accounts){
      System.out.println(account);
    }
  }
}
```
