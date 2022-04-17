pom.xml
```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.3.0</version>
</dependency>
```

application.yml
```yaml
pagehelper:
  helperDialect: mysql
  reasonable: true
  supportMethodsArguments: true
  params: count=countSql
```

service
```java
@Service
public class UserImpl implements User {
    @Autowired
    UserMapper userMapper;

    @Override
    public PageInfo<User> selectAll(int pageNum, int pageSize) {
        // 只有紧跟着PageHelper.startPage(pageNum,pageSize)的sql语句才会起作用
        PageHelper.startPage(pageNum, pageSize);
        List<User> users = userMapper.selectAll();
        return new PageInfo<>(users);
    }
}
```
