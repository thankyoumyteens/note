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

# Pointcut表达式

## execution表达式

```java
// 任何的public方法
@Pointcut("execution(public * *(..))")
// 以set开始的方法
@Pointcut("execution(* set*(..))")
// 定义在cn.freemethod.business.pack.Say接口中的方法
@Pointcut("execution(* cn.freemethod.business.pack.Say.*(..))")
// 任何cn.freemethod.business包中的方法
@Pointcut("execution(* cn.freemethod.business.*.*(..))")
// 任何定义在com.xyz.service包或者其子包中的方法
@Pointcut("execution(* cn.freemethod.business..*.*(..))")
```

## within表达式

```java
// 任何在com.xyz.service包中的方法
@Pointcut("within(com.xyz.service.*)")
// 任何定义在com.xyz.service包或者其子包中的方法
@Pointcut("within(com.xyz.service..*)")
```

## this表达式

```java
// 任何实现了com.xyz.service.AccountService接口中的方法
@Pointcut("this(com.xyz.service.AccountService)")
```

## target表达式

```java
// 任何目标对象实现了com.xyz.service.AccountService的方法
@Pointcut("target(com.xyz.service.AccountService)")
```

## args表达式

```java
// 有且只有一个Serializable参数的方法, 
// 只要这个参数实现了java.io.Serializable接口就可以，
// 不管是Serializable还是Integer，还是String都可以
@Pointcut("args(java.io.Serializable)")
```

## bean表达式

```java
// bean名字为simpleSay中的所有方法。
@Pointcut("bean(simpleSay)")
// bean名字匹配*Impl的bean中的所有方法。
@Pointcut("bean(*Impl)")
```

## 注解相关的表达式

```java
// 目标(target)使用了@Transactional注解的方法
@Pointcut("@target(org.springframework.transaction.annotation.Transactional)")
// 目标类(target)如果有Transactional注解中的所有方法
@Pointcut("@within(org.springframework.transaction.annotation.Transactional)")
// 任何方法有Transactional注解的方法
@Pointcut("@annotation(org.springframework.transaction.annotation.Transactional)")
// 有且仅有一个参数并且参数上类型上有Transactional注解, 
// 注意是参数类型上有Transactional注解，而不是方法的参数上有注解。
@Pointcut("@args(org.springframework.transaction.annotation.Transactional)")
```
