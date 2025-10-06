# 集成 MybatisPlus

### 1. 依赖

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
    <version>3.5.7</version>
</dependency>
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

### 2. 配置数据源

```yaml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/test?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&useSSL=false&serverTimezone=GMT%2B8&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&allowMultiQueries=true&useOldAliasMetadataBehavior=true&autoReconnect=true&failOverReadOnly=false
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
```

### 3. resource 下新建 mapper 文件夹

### 4. 配置 mybatis plus

```yaml
mybatis-plus:
  # 打印sql
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

### 5. 配置包扫描

```java
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("com.example.mapper")
public class MybatisPlusConfig {
}
```

### 6. 添加实体类

```java
import com.baomidou.mybatisplus.annotation.TableName;

@Data
// 表名和实体类名不一致时
// 可以手动指定表名
@TableName("words_info")
public class Words {
    // 指定主键
    @TableId(value = "words_id", type = IdType.NONE)
    private Integer wordsId;
    private String createTime;
    private String updateTime;
}
```

### 7. 添加 mapper 接口

```java
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

public interface DemoMapper extends BaseMapper<Words> {
}
```

### 8. 测试

```java
@Component
public class ConsoleApp implements CommandLineRunner {
    @Autowired
    private DemoMapper demoMapper;

    @Override
    public void run(String... args) throws Exception {
        Words existedWord = demoMapper.selectOne(Wrappers.<Words>query()
                    .eq("create_time", "2020-01-01"));
        System.out.println(existedWord);
    }
}
```
