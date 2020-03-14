# @Configuration
用于指定当前类是一个 spring 配置类,当创建容器时会从该类上加载注解。获取容器时需要使用
```java
@Configuration
public class SpringConfiguration { 
}
```

# @ComponentScan
用于指定 spring 在初始化容器时要扫描的包,我们使用此注解就等同于在xml中配置了:
```xml
<context:component-scan base-package="com.test"/>
```
```java
@Configuration 
@ComponentScan("com.test") 
  public class SpringConfiguration { 
}
```

# @Bean
该注解只能写在方法上,用于把此方法的返回值作为bean对象存入spring的ioc容器中
```java
// bean的id是dataSource
@Bean(name="dataSource") 
public DataSource createDataSource() { 
  // ...
  return dataSource;
}
```

# @PropertySource
用于加载.properties 文件中的配置。例如我们配置数据源时,可以把连接数据库的信息写到
properties 配置文件中,就可以使用此注解指定 properties 配置文件的位置
```java
@Configuration
@PropertySource("classpath:jdbc.properties")
public class JdbcConfig { 
  @Value("${jdbc.driver}") 
  private String driver; 
  @Value("${jdbc.url}") 
  private String url; 
  @Value("${jdbc.username}") 
  private String username; 
  @Value("${jdbc.password}") 
  private String password; 
 
  @Bean(name="dataSource") 
  public DataSource createDataSource() { 
    try { 
      ComboPooledDataSource ds = new ComboPooledDataSource(); 
      ds.setDriverClass(driver); 
      ds.setJdbcUrl(url); 
      ds.setUser(username); 
      ds.setPassword(password); 
      return ds; 
    } catch (Exception e) { 
      throw new RuntimeException(e); 
    } 
  }   
} 
```

# @Import
用于导入其他配置类
```java
@Configuration 
@ComponentScan(basePackages="com.test") 
@Import({JdbcConfig.class})
public class SpringConfiguration { 
}
```

# 加载配置
```java
// 从类的根路径下加载配置文件
ApplicationContext ac = new AnnotationApplicationContext(SpringConfiguration.class);
// 根据 bean 的 id 获取对象
IAccountService aService = (IAccountService) ac.getBean("accountService");
IAccountDao aDao = ac.getBean("accountDao", IAccountDao.class);
```
