# 集成 Mybatis

1. 依赖

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>
```

2. 配置数据源

```yaml
spring:
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/test?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&useSSL=false&serverTimezone=GMT%2B8&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&allowMultiQueries=true&useOldAliasMetadataBehavior=true&autoReconnect=true&failOverReadOnly=false
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
```

3. resource 下新建 mapper 文件夹
4. 配置 mybatis 的 xml

```yaml
mybatis:
  mapper-locations: classpath*:mapper/*.xml
```

5. 配置包扫描

```java
package com.example;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("com.example.mapper")
public class MybatisConfig {
}
```

6. 添加 mapper 接口

```java
package com.example.mapper;

import java.util.List;
import java.util.Map;

public interface DemoMapper {
    List<Map<String, Object>> selectAll();
}
```

7. 添加 sql

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.mapper.DemoMapper">

    <select id="selectAll" resultType="java.util.Map">
        select *
        from user
    </select>
</mapper>
```

8. 测试

```java
package com.example;

import com.example.mapper.DemoMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class ConsoleApp implements CommandLineRunner {
    @Autowired
    private DemoMapper demoMapper;

    @Override
    public void run(String... args) throws Exception {
        System.out.println(demoMapper.selectAll());
    }
}
```
