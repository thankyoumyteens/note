# springboot+自定义注解实现灵活的切面配置

加入相关maven依赖
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

控制器
```java
@RestController
public class HelloController {
    @RequestMapping("/add1")  
    public String addData1(String deviceId) {
        return "success";
    }
    @RequestMapping("/add2")  
    public String addData2(String deviceId) {
        return "success";
    }
}
```

添加一个自定义注解
```java
@Documented 
@Retention(RetentionPolicy.RUNTIME) 
@Target(ElementType.METHOD) 
public @interface MyAnnotation {
}
```

配置切面
```java
@Aspect
@Component
public class TestAspect {
    @Pointcut("@annotation(com.example.demo.controller.MyAnnotation)" )
    public void addAdvice(){}  
    @Around("addAdvice()")
    public Object Interceptor(ProceedingJoinPoint pjp){
        Object result = null; 
        Object[] args = pjp.getArgs();
        try {
            result =pjp.proceed();
        } catch (Throwable e) {
            e.printStackTrace();
        }  
        return result;
    }
}
```

修改控制器，给需要切面的方法上加上注解
```java
@RestController
public class HelloController {
    @MyAnnotation
    @RequestMapping("/add1") 
    public String addData1(String deviceId) {
        return "success";
    }
    @RequestMapping("/add2") 
    public String addData2(String deviceId) {
        return "success";
    }
}
```
