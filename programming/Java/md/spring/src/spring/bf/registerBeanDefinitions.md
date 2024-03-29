# 开始注册 BeanDefinition

在 Spring 中，xml 的命名空间主要分为默认命名空间和自定义命名空间。默认命名空间包括"import", "alias", "bean"以及"beans"标签。另一方面，自定义命名空间是 Spring 的一个重要设计，它为第三方应用提供了充分的拓展空间。比如`<context:annotation-config />`。

注册 BeanDefinition 的过程：

1. 从根节点开始遍历 xml 配置文件的每个节点
2. 判断节点是否是默认命名空间，如果是，则交给 parseDefaultElement 处理
3. 判断节点是否是自定义命名空间，如果是，则交给 parseCustomElement 处理

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    // 注册BeanDefinition
    public int registerBeanDefinitions(Document doc, Resource resource)
            throws BeanDefinitionStoreException {
        BeanDefinitionDocumentReader documentReader = createBeanDefinitionDocumentReader();
        // 查询之前已经注册了多少BeanDefinition
        int countBefore = getRegistry().getBeanDefinitionCount();
        // 注册BeanDefinition
        documentReader.registerBeanDefinitions(doc, createReaderContext(resource));
        // 记录本次注册了多少BeanDefinition
        return getRegistry().getBeanDefinitionCount() - countBefore;
    }
}

public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    public void registerBeanDefinitions(Document doc, XmlReaderContext readerContext) {
        this.readerContext = readerContext;
        // 获取xml根节点
        Element root = doc.getDocumentElement();
        // 注册BeanDefinition
        doRegisterBeanDefinitions(root);
    }

    protected void doRegisterBeanDefinitions(Element root) {
        BeanDefinitionParserDelegate parent = this.delegate;
        this.delegate = createDelegate(getReaderContext(), root, parent);

        if (this.delegate.isDefaultNamespace(root)) {
            // 处理profile属性，profile属性用于配置不同的环境，比如：生产环境和开发环境
            String profileSpec = root.getAttribute(PROFILE_ATTRIBUTE);
            if (StringUtils.hasText(profileSpec)) {
                String[] specifiedProfiles = StringUtils.tokenizeToStringArray(
                        profileSpec, BeanDefinitionParserDelegate.MULTI_VALUE_ATTRIBUTE_DELIMITERS);
                // 判断是否启用了profile，如果设置了profile，但是没有一个启用的，则直接返回
                if (!getReaderContext().getEnvironment().acceptsProfiles(specifiedProfiles)) {
                    return;
                }
            }
        }
        // 设计模式：模版方法模式
        // 注册BeanDefinition前的处理，空方法，留给子类实现
        preProcessXml(root);
        // 解析bean标签
        parseBeanDefinitions(root, this.delegate);
        // 注册BeanDefinition后的处理，空方法，留给子类实现
        postProcessXml(root);

        this.delegate = parent;
    }

    protected void parseBeanDefinitions(Element root, BeanDefinitionParserDelegate delegate) {
        if (delegate.isDefaultNamespace(root)) {
            // 解析默认命名空间的标签
            NodeList nl = root.getChildNodes();
            // 遍历子标签
            for (int i = 0; i < nl.getLength(); i++) {
                Node node = nl.item(i);
                if (node instanceof Element) {
                    Element ele = (Element) node;
                    if (delegate.isDefaultNamespace(ele)) {
                        // 解析默认命名空间的标签
                        // 比如：<bean id="myTestBean" class="bean.MyTestBean">
                        parseDefaultElement(ele, delegate);
                    } else {
                        // 解析自定义命名空间的标签
                        // 比如：<tx:annotation-driven />
                        delegate.parseCustomElement(ele);
                    }
                }
            }
        } else {
            // 解析自定义命名空间的标签
            delegate.parseCustomElement(root);
        }
    }
}
```
