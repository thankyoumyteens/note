# 使用BeanFactory

maven依赖：

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.2.5.RELEASE</version>
</dependency>
```

定义bean：

```java
public class MyTestBean { 
    private String testStr = "testStr"; 
    public String getTestStr() {
        return testStr;
    }
    public void setTestStr(String testStr) {
        this.testStr = testStr;
    }
}
```

配置文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/Spring-beans.xsd">
    <bean id="myTestBean" class="bean.MyTestBean">
</beans> 
```

测试代码：

```java
public class BeanFactoryTest {
    @Test
    public void testSimpleLoad() {
        // 读取xml配置文件
        Resource resource = new ClassPathResource("beanFactoryTest.xml");
        // 加载bean
        BeanFactory bf = new XmlBeanFactory(resource);
        // 获取bean
        MyTestBean bean = (MyTestBean) bf.getBean("myTestBean");
        assertEquals("testStr", bean.getTestStr());
    }
}
```

