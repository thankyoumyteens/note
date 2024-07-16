# 延迟加载

延迟加载(懒加载)是指在进行关联查询时，不会执行对关联对象的查询, 而是在真正访问关联对象的信息时才去查询。

Mybatis 在实现懒加载时要使用 resultMap，不能使用 resultType。resultMap 中, 一对一关联的 association 和一对多的 collection 可以实现懒加载。

## 实现原理

以下面的类为例:

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User implements Serializable {
    private Integer id;
    private String username;
    // 一对多
    private List<Account> accounts;
}
```

1. 使用 cglib 创建 User 类的代理对象
2. 当调用 getAccounts 方法时进入拦截器 invoke 方法, 如果 accounts 为 null, 则执行 sql 获取 accounts 的数据
3. 然后调用 setAccounts 方法填充数据, 最后返回 accounts 数据
