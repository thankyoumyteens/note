# 多数据源

1. 配置文件

```yaml
demo1:
  datasource:
    # 数据源1
    mariadb01:
      # 注意这里要用jdbc-url
      jdbc-url: jdbc:mariadb://127.0.0.1:3306/db_test?characterEncoding=utf-8&useSSL=false&useTimezone=true&serverTimezone=GMT%2B8
      username: root
      password: 123456
      driver-class-name: org.mariadb.jdbc.Driver
    # 数据源2
    sqlite02:
      # 注意这里要用jdbc-url
      jdbc-url: jdbc:sqlite:/home/words.db
      driver-class-name: org.sqlite.JDBC
mybatis:
  # 打印sql
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

2. 数据源 1 的配置类

```java
package com.example;

import com.zaxxer.hikari.HikariDataSource;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;

import javax.sql.DataSource;

@Configuration
// 配置mapper扫描路径，指定mariadb01的SqlSessionFactory
@MapperScan(basePackages = "com.example.mapper.mariadb01", sqlSessionFactoryRef = "mariadb01SqlSessionFactory")
public class Mariadb01Config {

    /**
     * 配置数据源 mariadb01
     */
    @Bean(name = "mariadb01DataSource")
    // 加载demo1.datasource.mariadb01的配置到HikariDataSource
    @ConfigurationProperties(prefix = "demo1.datasource.mariadb01")
    public DataSource mariadb01DataSource() {
        return new HikariDataSource();
    }

    /**
     * 配置事务
     *
     * @param dataSource 传入mariadb01数据源
     */
    @Bean(name = "mariadb01TransactionManager")
    public DataSourceTransactionManager mariadb01TransactionManager(@Qualifier("mariadb01DataSource") DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }

    /**
     * 配置mariadb01的SqlSessionFactory
     *
     * @param dataSource 传入mariadb01数据源
     */
    @Bean(name = "mariadb01SqlSessionFactory")
    public SqlSessionFactory mariadb01SqlSessionFactory(@Qualifier("mariadb01DataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
        // 设置数据源
        factoryBean.setDataSource(dataSource);
        // 设置mapper xml的路径
        factoryBean.setMapperLocations(new PathMatchingResourcePatternResolver()
                .getResources("classpath:mapper/mariadb01/*.xml"));
        return factoryBean.getObject();
    }

}
```

2. 数据源 2 的配置类

```java
package com.example;

import com.zaxxer.hikari.HikariDataSource;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;

import javax.sql.DataSource;

@Configuration
// 配置mapper扫描路径，指定sqlite02的SqlSessionFactory
@MapperScan(basePackages = "com.example.mapper.sqlite02", sqlSessionFactoryRef = "sqlite02SqlSessionFactory")
public class Sqlite02Config {

    /**
     * 配置数据源 sqlite02
     */
    @Bean(name = "sqlite02DataSource")
    // 加载demo1.datasource.sqlite02的配置到HikariDataSource
    @ConfigurationProperties(prefix = "demo1.datasource.sqlite02")
    public DataSource sqlite02DataSource() {
        return new HikariDataSource();
    }

    /**
     * 配置事务
     *
     * @param dataSource 传入sqlite02数据源
     */
    @Bean(name = "sqlite02TransactionManager")
    public DataSourceTransactionManager sqlite02TransactionManager(@Qualifier("sqlite02DataSource") DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }

    /**
     * 配置sqlite02的SqlSessionFactory
     *
     * @param dataSource 传入sqlite02数据源
     */
    @Bean(name = "sqlite02SqlSessionFactory")
    public SqlSessionFactory sqlite02SqlSessionFactory(@Qualifier("sqlite02DataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
        // 设置数据源
        factoryBean.setDataSource(dataSource);
        // 设置mapper xml的路径
        factoryBean.setMapperLocations(new PathMatchingResourcePatternResolver()
                .getResources("classpath:mapper/sqlite02/*.xml"));
        return factoryBean.getObject();
    }
}
```

3. 为不同数据源创建不同的 mapper 文件夹和 mapper 包
4. 使用不同的 mapper

```java
@Component
public class ConsoleApp implements CommandLineRunner {
    @Autowired
    private WordsMapper wordsMapper;
    @Autowired
    private BookMapper bookMapper;

    @Override
    public void run(String... args) throws Exception {
        List<Map<String, Object>> words = wordsMapper.selectAll();
        System.out.println(words);
        System.out.println("--------------------------------------------------");
        List<Map<String, Object>> books = bookMapper.selectAll();
        System.out.println(books);
    }
}
```
