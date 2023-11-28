# replaced-method

replaced-method 可以在运行时用新的方法替换现有的方法。

## replaced-method 的用法

1. 创建要被替换的方法: 

```java
public class TestChangeMethod {

    public void changeMe() {
        System.out.println("change me");
    }
}
```

2. 创建替换方法: 

```java
// 需要实现MethodReplacer接口
public class TestMethodReplacer implements MethodReplacer {
    @Override
    public Object reimplement(Object o, Method method, Object[] objects) throws Throwable {
        System.out.println("替换原有的方法");
        return null;
    }
}
```

3. 创建测试方法: 

```java
public static void main(String[] args) {
    ApplicationContext ac = new ClassPathXmlApplicationContext("testReplace.xml");
    TestChangeMethod test = (TestChangeMethod) ac.getBean("testChangeMethod");
    test.changeMe();
}
```

4. 配置文件: 

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="testReplacer" class="test.replaced.TestMethodReplacer" />
    <!-- changeMe()方法会被替换为reimplement()方法 -->
    <bean id="testChangeMethod" class="test.replaced.TestChangeMethod">
        <replaced-method name="changeMe" replacer="testReplacer"/>
    </bean>
</beans>
```

5. 输出结果: 

```
替换原有的方法
```
