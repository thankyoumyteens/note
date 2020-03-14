# 启用AOP
```java
@Configuration 
@ComponentScan(basePackages="com.test") 
@EnableAspectJAutoProxy 
public class SpringConfiguration { 
}
```

# 配置通知类
```java
@Component("txManager") 
@Aspect // 表明当前类是一个切面类
public class TransactionManager {
  // 切入点表达式
  @Pointcut("execution(* com.test.service.impl.*.*(..))") 
  private void pt1() {} 
  // 配置前置通知
  @Before("pt1()") 
  public void beginTransaction() { 
  } 
  // 配置后置通知
  @AfterReturning("pt1()") 
  public void commit() { 
  } 
  // 配置异常通知
  @AfterThrowing("pt1()") 
  public void rollback() { 
  } 
  // 配置最终通知
  @After("pt1()") 
  public void release() { 
  } 

  // 环绕通知
  @Around("pt1()") 
  public Object transactionAround(ProceedingJoinPoint pjp) { 
    //定义返回值 
    Object rtValue = null; 
    try { 
      //获取方法执行所需的参数 
      Object[] args = pjp.getArgs(); 
      //前置通知：开启事务 
      beginTransaction(); 
      //执行方法 
      rtValue = pjp.proceed(args); 
      //后置通知：提交事务 
      commit(); 
    }catch(Throwable e) { 
      //异常通知：回滚事务 
      rollback(); 
    }finally { 
      //最终通知：释放资源 
      release(); 
    }
    return rtValue; 
  } 
} 
```
