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
@ContextConfiguration(locations= {"classpath:spring/bean.xml"})
// 批量指定: @ContextConfiguration(locations= {"classpath:spring/*"})
public class AccountServiceTest {}
```

# 使用@Autowired 注入数据
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations= {"classpath:spring/*"})
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

# 常见错误

## NoSuchBeanDefinitionException

可能的原因: 包扫描配置错误, 导致bean没被加载到spring中

解决
```xml
<!-- 不要使用com.base..* -->
<context:component-scan
	base-package="com.base"/>
```

## FileNotFoundException

原因: 使用junit时不会加载webapp目录下的文件

解决: 将WEB-INF文件夹整个拷贝到test下的resources目录下

