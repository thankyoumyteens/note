# Maven依赖

```xml
<!-- 1.Spring核心依赖 -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>4.3.7.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-beans</artifactId>
    <version>4.3.7.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>4.3.7.RELEASE</version>
</dependency>
```

# 创建Spring配置类

```java
package org.example;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
// 指定 spring 在初始化容器时要扫描的包
@ComponentScan("org.example.test")
public class SpringConfiguration {
}
```

# 使用@Component创建Bean

需要在@ComponentScan指定的包下

```java
package org.example.test;

import org.springframework.stereotype.Component;

@Component
public class Test {

    public void test() {
        System.out.println("ok");
    }
}
```

# 创建启动类

```java
package org.example;

import org.example.test.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class App {
    public static void main(String[] args) {
        ApplicationContext ac = new AnnotationConfigApplicationContext(SpringConfiguration.class);
        Test test = ac.getBean(Test.class);
        test.test();
    }
}
```

# 使用@Bean创建Bean

```java
@Configuration
// 加载.properties文件中的配置
@PropertySource("classpath:jdbc.properties")
public class SpringConfiguration {

    @Value("${jdbc.driver}")
    private String driver;
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.username}")
    private String username;
    @Value("${jdbc.password}")
    private String password;

    @Bean(name = "dataSource")
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

# 导入其他配置类

```java
// 被导入的配置类
@Configuration
public class JdbcConfig {
}
```

```java
@Configuration 
// 导入JdbcConfig配置类
@Import({JdbcConfig.class})
public class SpringConfiguration { 
}
```
