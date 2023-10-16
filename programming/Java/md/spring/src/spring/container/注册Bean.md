# 注册Bean

通过SAX解析完xml配置文件后，就会调用了XregisterBeanDefinitions()方法去注册bean：

> spring-framework-5.0.x\spring-beans\src\main\java\org\springframework\beans\factory\xml\XmlBeanDefinitionReader.java

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

> spring-framework-5.0.x\spring-beans\src\main\java\org\springframework\beans\factory\xml\DefaultBeanDefinitionDocumentReader.java

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
}
```
