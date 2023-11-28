# lookup-method

lookup-method 是一种特殊的方法注入, 它把一个方法声明为返回某种类型的 bean, 但实际要返回的 bean 是在配置文件里面配置的。

## lookup-method 的用法

1. 创建一个父类: 

```java
public class User {
    public void showMe() {
        System.out.printf("i am user");
    }
}
```

2. 创建一个子类, 并覆盖 showMe()方法: 

```java
public class Teacher extends User {
    public void showMe() {
        System.out.printf("i am teacher");
    }
}
```

3. 创建调用方法: 

```java
public abstract class GetBeanTest {

    // 这里的抽象方法不需要实现
    public abstract User getBean();

    public void showMe() {
        getBean().showMe();
    }
}
```

4. 创建测试方法: 

```java
public static void main(String[] args) {
    ApplicationContext ac = new ClassPathXmlApplicationContext("lookupTest.xml");
    GetBeanTest test = (GetBeanTest) ac.getBean("getBeanTest");
    test.showMe();
}
```

5. xml 配置文件: 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="teacher" class="test.lookup.bean.Teacher" />
    <!-- lookup-method会动态地将teacher所代表的bean作为getBean的返回值 -->
    <!-- 当需要使用其他类时, 只需要把lookup-method的bean属性换成相应的类即可 -->
    <bean id="getBeanTest" class="test.lookup.app.GetBeanTest">
        <lookup-method name="getBean" bean="teacher" />
    </bean>
　　
</beans>
```

6. 运行结果: 

```
i am teacher
```
