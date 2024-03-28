# @Transactional 应用在非 public 修饰的方法上

在Spring AOP 代理时, TransactionInterceptor(事务拦截器)在目标方法执行前后进行拦截, DynamicAdvisedInterceptor(CglibAopProxy 的内部类)的 intercept 方法或 JdkDynamicAopProxy 的 invoke 方法会间接调用 AbstractFallbackTransactionAttributeSource 的 computeTransactionAttribute方法, 获取Transactional 注解的事务配置信息。此方法会检查目标方法的修饰符是否为 public, 不是 public则不会获取@Transactional 的属性配置信息。

# @Transactional 注解属性 propagation 设置错误

若是配置以下三种 propagation, 事务将不会发生回滚。

1. TransactionDefinition.PROPAGATION_SUPPORTS: 如果当前存在事务, 则加入该事务；如果当前没有事务, 则以非事务的方式继续运行。
1. TransactionDefinition.PROPAGATION_NOT_SUPPORTED: 以非事务方式运行, 如果当前存在事务, 则把当前事务挂起。
1. TransactionDefinition.PROPAGATION_NEVER: 以非事务方式运行, 如果当前存在事务, 则抛出异常。

# @Transactional 注解属性 rollbackFor 设置错误

rollbackFor 可以指定能够触发事务回滚的异常类型。Spring默认抛出了unchecked异常(继承自 RuntimeException)或者 Error 才回滚事务；其他异常不会触发回滚事务。如果在事务中抛出其他类型的异常, 但却期望 Spring 能够回滚事务, 就需要指定 rollbackFor属性。若在目标方法中抛出的异常是 rollbackFor 指定的异常的子类, 事务同样会回滚。

# 同一个类中方法调用, 导致@Transactional失效

比如有一个类Test, 它的一个方法A, A再调用本类的方法B(不论方法B是用public还是private修饰), 但方法A没有声明注解事务, 而B方法有。则外部调用方法A之后, 方法B的事务是不会起作用的。这也是经常犯错误的一个地方。

```java
public class Demo {

    public void A() {
        B();
    }

    @Transactional
    public void B() {
        // @Transactional失效
    }
}
```

这是由于使用Spring AOP代理造成的, 因为只有当事务方法被当前类以外的代码调用时, 才会由Spring生成的代理对象来管理。

```java
public class Caller {
    @Autowired
    Callee ee;

    public void A() {
        ee.B();
    }
}

public class Callee {
    @Transactional
    public void B() {
        // @Transactional生效
    }
}
```

# 异常被你的 catch吃了, 导致@Transactional失效

如果B方法内部抛了异常, 而A方法此时try catch了B方法的异常, 那这个事务不能正常回滚

# 数据库引擎不支持事务

这种情况出现的概率并不高
