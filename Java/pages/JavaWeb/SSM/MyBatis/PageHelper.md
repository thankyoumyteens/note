# PageHelper用法

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

# PageHelper.startPage工作原理

PageHelper会用ThreadLocal将分页信息保存在当前线程中

PageHelper配置了MyBatis的拦截器，在执行sql前会读取出分页信息，为sql加上limit

# new PageInfo<>() 可以获取到页码、页大小、总页数等信息的原因

使用了`PageHelper.startPage`之后，查询出的List是`Page<T>`类型

Page类是ArrayList的子类：
```java
public class Page<E> extends ArrayList<E> implements Closeable {
    private static final long serialVersionUID = 1L;

    /**
     * 页码，从1开始
     */
    private int pageNum;
    /**
     * 页面大小
     */
    private int pageSize;
    ...
```

所以在new PageInfo<>(list)的时候可以把页码、页大小、总页数等信息给PageInfo

