# 注解
告知spring框架在读取配置文件创建容器时, 扫描指定包com.test下的类, 依据类中使用的注解创建对象, 并存入容器中
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/context
    http://www.springframework.org/schema/context/spring-context.xsd">
  <context:component-scan base-package="com.test"/>
</beans>
```

# 用于创建对象的注解
他们的作用就和在XML配置文件中编写一个bean标签实现的功能是一样的
- @Component 用于把当前类对象存入spring容器中
- @Controller 一般用在表现层,作用和属性与Component一样
- @Service 一般用在业务层,作用和属性与Component一样
- @Repository 一般用在持久层,作用和属性与Component一样
```java
// 把Demo1存入spring容器中
// bean的id是demo1
@Component('demo1')
public class Demo1 {
  // ...
}
```
