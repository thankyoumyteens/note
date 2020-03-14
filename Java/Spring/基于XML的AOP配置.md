# 引入依赖
```xml
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-context</artifactId>
  <version>5.0.2.RELEASE</version>
</dependency>
<dependency>
  <groupId>org.aspectj</groupId>
  <artifactId>aspectjweaver</artifactId>
  <version>1.8.7</version>
</dependency>
```

# 切入点表达式(为哪个方法添加切面)
```java
// 标准的表达式写法
execution(public void com.test.service.impl.AccountServiceImpl.saveAccount())
// 访问修饰符可以省略
execution(void com.test.service.impl.AccountServiceImpl.saveAccount())
// 返回值使用通配符
execution(* com.test.service.impl.AccountServiceImpl.saveAccount())
// 包名可以使用通配符
execution(* *.*.*.*.AccountServiceImpl.saveAccount()))
// 包名可以使用..表示当前包及其子包
execution(* *..AccountServiceImpl.saveAccount())
// 类名和方法名都可以使用*来实现通配
execution(* *..*.*())
// 参数列表
execution(* *..AccountServiceImpl.saveAccount(java.lang.String))
// 可以使用..表示有无参数均可
execution(* *..*.*(..))
// 表示业务层实现类下的所有方法
execution(* com.test.service.impl.*.*(..))
```

# 配置AOP, 使service的每个方法调用之前都执行Logger的printLog方法
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:aop="http://www.springframework.org/schema/aop"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop.xsd">
  <!-- 配置srping的Ioc,把service对象配置进来-->
  <bean id="accountService" class="com.test.service.impl.AccountServiceImpl"/>
  <!-- 配置Logger类 -->
  <bean id="logger" class="com.test.utils.Logger"/>
  
  <!--配置AOP-->
  <aop:config>
    <!--配置切面 -->
    <aop:aspect id="logAdvice" ref="logger">
      <!-- aop:before 配置通知的类型
        method logger类中的printLog方法
        pointcut 指定切入点方法 -->
      <aop:before method="printLog" pointcut="execution(* com.test.service.impl.*.*(..))"/>
    </aop:aspect>
  </aop:config>
</beans>
```
