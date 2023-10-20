# 解析lookup-method子标签

lookup-method是一种特殊的方法注入，它把一个方法声明为返回某种类型的bean，但实际要返回的bean是在配置文件里面配置的。

## lookup-method的用法

1. 创建一个父类：

```java
public class User {
    public void showMe() {
        System.out.printf("i am user");
    }
}
```

2. 创建一个子类，并覆盖showMe()方法：

```java
public class Teacher extends User {
    public void showMe() {
        System.out.printf("i am teacher");
    }
}
```

3. 创建调用方法：

```java
public abstract class GetBeanTest {

    // 这里的抽象方法不需要实现
    public abstract User getBean();

    public void showMe() {
        getBean().showMe();
    }
}
```

4. 创建测试方法：

```java
public static void main(String[] args) {
    ApplicationContext ac = new ClassPathXmlApplicationContext("lookupTest.xml");
    GetBeanTest test = (GetBeanTest) ac.getBean("getBeanTest");
    test.showMe();
}
```

5. xml配置文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="teacher" class="test.lookup.bean.Teacher" />
    <!-- lookup-method会动态地将teacher所代表的bean作为getBean的返回值 -->
    <!-- 当需要使用其他类时，只需要把lookup-method的bean属性换成相应的类即可 -->
    <bean id="getBeanTest" class="test.lookup.app.GetBeanTest">
        <lookup-method name="getBean" bean="teacher" />
    </bean>
　　
</beans>
```

6. 运行结果：

```
i am teacher
```

## 解析lookup-method标签

```java
public class BeanDefinitionParserDelegate {

    public void parseLookupOverrideSubElements(Element beanEle, MethodOverrides overrides) {
        NodeList nl = beanEle.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            // lookup-method标签只有在bean标签内才生效
            if (isCandidateElement(node) && nodeNameEquals(node, LOOKUP_METHOD_ELEMENT)) {
                Element ele = (Element) node;
                // 获取配置返回的bean
                String methodName = ele.getAttribute(NAME_ATTRIBUTE);
                String beanRef = ele.getAttribute(BEAN_ELEMENT);
                LookupOverride override = new LookupOverride(methodName, beanRef);
                override.setSource(extractSource(ele));
                // 保存到BeanDefinition的methodOverrides字段中
                overrides.addOverride(override);
            }
        }
    }
}
```
