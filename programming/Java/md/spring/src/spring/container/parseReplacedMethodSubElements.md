# 解析replaced-method子标签

replaced-method可以在运行时用新的方法替换现有的方法。

## replaced-method的用法

1. 创建要被替换的方法：

```java
public class TestChangeMethod {

    public void changeMe() {
        System.out.println("change me");
    }
}
```

2. 创建替换方法：

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

3. 创建测试方法：

```java
public static void main(String[] args) {
    ApplicationContext ac = new ClassPathXmlApplicationContext("testReplace.xml");
    TestChangeMethod test = (TestChangeMethod) ac.getBean("testChangeMethod");
    test.changeMe();
}
```

4. 配置文件：

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

5. 输出结果：

```
替换原有的方法
```

## 解析replaced-method标签

parseReplacedMethodSubElements()方法会解析bean的replaced-method子标签。

```java
public class BeanDefinitionParserDelegate {

    public void parseReplacedMethodSubElements(Element beanEle, MethodOverrides overrides) {
        NodeList nl = beanEle.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            // replaced-method标签只有在bean标签内才生效
            if (isCandidateElement(node) && nodeNameEquals(node, REPLACED_METHOD_ELEMENT)) {
                Element replacedMethodEle = (Element) node;
                // 要替换的旧方法
                String name = replacedMethodEle.getAttribute(NAME_ATTRIBUTE);
                // 新方法
                String callback = replacedMethodEle.getAttribute(REPLACER_ATTRIBUTE);
                ReplaceOverride replaceOverride = new ReplaceOverride(name, callback);
                // 如果有参数，就记录参数
                List<Element> argTypeEles = DomUtils.getChildElementsByTagName(replacedMethodEle, ARG_TYPE_ELEMENT);
                for (Element argTypeEle : argTypeEles) {
                    String match = argTypeEle.getAttribute(ARG_TYPE_MATCH_ATTRIBUTE);
                    match = (StringUtils.hasText(match) ? match : DomUtils.getTextValue(argTypeEle));
                    if (StringUtils.hasText(match)) {
                        replaceOverride.addTypeIdentifier(match);
                    }
                }
                replaceOverride.setSource(extractSource(replacedMethodEle));
                // 保存到BeanDefinition的methodOverrides字段中
                overrides.addOverride(replaceOverride);
            }
        }
    }
}
```
