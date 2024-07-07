# AOP

1. 记录操作日志, 用环绕通知记录参数和返回值
2. Spring 中的事务就是用 AOP 实现的

## 通过注解使用

1. 依赖

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>6.1.9</version>
</dependency>
<dependency>
    <groupId>org.aspectj</groupId>
    <artifactId>aspectjweaver</artifactId>
    <version>1.9.22.1</version>
</dependency>
```

2. 启用 AspectJ

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

@Configuration
@EnableAspectJAutoProxy
public class AopConfig {
}
```

3. 定义 Aspect

```java
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Component
@Aspect
public class LogAspect {

    // 表示匹配所有方法
    @Pointcut(value = "execution(* *(..))")
    private void pointcut() {
    }

    // 环绕通知
    @Around("pointcut()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("param is: " + Arrays.toString(joinPoint.getArgs()));
        Object result = joinPoint.proceed();
        System.out.println("result is: " + result);
        return result;
    }
}
```

4. 定义 service

```java
import org.springframework.stereotype.Service;

@Service
public class TestService {

    public String doSomething(String param) {
        return "hello " + param;
    }

}
```

5. 测试

```java
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class AopTest {

    public static void main(String[] args) {
        AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext("org.example.aopdemo");
        TestService testService = ac.getBean(TestService.class);
        System.out.println(testService.doSomething("test"));
    }
}
```
