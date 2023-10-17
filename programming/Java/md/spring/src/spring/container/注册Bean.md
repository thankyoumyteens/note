# 注册Bean

通过SAX解析完xml配置文件后，就会调用了XregisterBeanDefinitions()方法去注册bean：

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {
    
    // 注册bean
    public int registerBeanDefinitions(Document doc, Resource resource) 
            throws BeanDefinitionStoreException {
        // 创建一个DefaultBeanDefinitionDocumentReader对象
        BeanDefinitionDocumentReader documentReader = createBeanDefinitionDocumentReader();
        // 查询之前已经加载了多少bean
        int countBefore = getRegistry().getBeanDefinitionCount();
        // 加载及注册bean
        documentReader.registerBeanDefinitions(doc, createReaderContext(resource));
        // 记录本次加载了多少bean
        return getRegistry().getBeanDefinitionCount() - countBefore;
    }
}
```

## 加载及注册bean

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    public void registerBeanDefinitions(Document doc, XmlReaderContext readerContext) {
        this.readerContext = readerContext;
        // 获取xml根节点
        Element root = doc.getDocumentElement();
        // 开始注册bean
        doRegisterBeanDefinitions(root);
    }

    protected void doRegisterBeanDefinitions(Element root) {
        BeanDefinitionParserDelegate parent = this.delegate;
        this.delegate = createDelegate(getReaderContext(), root, parent);

        if (this.delegate.isDefaultNamespace(root)) {
            // 解析profile属性，profile属性用于配置不同的环境来适用于生产环境和开发环境
            String profileSpec = root.getAttribute(PROFILE_ATTRIBUTE);
            if (StringUtils.hasText(profileSpec)) {
                String[] specifiedProfiles = StringUtils.tokenizeToStringArray(
                        profileSpec, BeanDefinitionParserDelegate.MULTI_VALUE_ATTRIBUTE_DELIMITERS);
                if (!getReaderContext().getEnvironment().acceptsProfiles(specifiedProfiles)) {
                    return;
                }
            }
        }
        // 设计模式：模版方法模式
        // 解析前的处理，留给子类实现
        preProcessXml(root);
        // 解析并注册BeanDefinition
        parseBeanDefinitions(root, this.delegate);
        // 解析后的处理，留给子类实现
        postProcessXml(root);

        this.delegate = parent;
    }

    protected void parseBeanDefinitions(Element root, BeanDefinitionParserDelegate delegate) {
        if (delegate.isDefaultNamespace(root)) {
            NodeList nl = root.getChildNodes();
            for (int i = 0; i < nl.getLength(); i++) {
                Node node = nl.item(i);
                if (node instanceof Element) {
                    Element ele = (Element) node;
                    if (delegate.isDefaultNamespace(ele)) {
                        // 解析默认命名空间的标签
                        // 比如：<bean id="myTestBean" class="bean.MyTestBean">
                        parseDefaultElement(ele, delegate);
                    }
                    else {
                        // 解析自定义命名空间的标签
                        // 比如：<tx:annotation-driven />
                        delegate.parseCustomElement(ele);
                    }
                }
            }
        }
        else {
            // 解析自定义命名空间的标签
            delegate.parseCustomElement(root);
        }
    }
}
```

在Spring框架中，命名空间主要分为默认命名空间和自定义命名空间。

默认命名空间包括"import", "alias", "bean"以及"beans"等标签。

另一方面，自定义命名空间是Spring的一个重要设计，它为第三方应用提供了充分的拓展空间。例如，常见的各种集成框架如dubbo、mybatis等，就会有自己的命名空间。

Spring在解析这些命名空间时，会调用对应的方法进行解析。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/mvc
    http://www.springframework.org/schema/mvc/spring-mvc.xsd
    http://www.springframework.org/schema/context
    http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 启用spring mvc 注解，使用的是自定义命名空间：context -->
    <context:annotation-config />

    <!-- 设置使用注解的类所在的jar包，使用的是自定义命名空间：context -->
    <context:component-scan base-package="controller"></context:component-scan>

    <!-- 完成请求和注解POJO的映射，使用的是默认命名空间 -->
    <bean class="org.springframework.web.servlet.mvc.annotation.AnnotationMethodHandlerAdapter" />
　　
    <!-- 对转向页面的路径解析，使用的是默认命名空间 -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver" p:prefix="/jsp/" p:suffix=".jsp" />
</beans>
```
