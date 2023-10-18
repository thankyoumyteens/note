# 解析bean标签下的自定义标签

bean标签下的自定义标签：

```xml
<bean id="testBean" class="test.TestBean">
  <mybean:user username="123"/>
</bean>
```

bean标签下的自定义标签会委托给BeanDefinitionParserDelegate::decorateBeanDefinitionIfRequired()方法解析。

```java
public class BeanDefinitionParserDelegate {

    public BeanDefinitionHolder decorateBeanDefinitionIfRequired(Element ele, BeanDefinitionHolder originalDef) {
        // 第三个参数是为了使用父类的scope属性，
        // 以备子类若没有设置scope时默认使用父类的属性，
        // 这里解析的是顶层bean，所以传null
        return decorateBeanDefinitionIfRequired(ele, originalDef, null);
    }

    public BeanDefinitionHolder decorateBeanDefinitionIfRequired(
            Element ele, BeanDefinitionHolder originalDef, @Nullable BeanDefinition containingBd) {

        BeanDefinitionHolder finalDefinition = originalDef;

        // 遍历所有的属性，看是否有适用于修饰的属性
        NamedNodeMap attributes = ele.getAttributes();
        for (int i = 0; i < attributes.getLength(); i++) {
            Node node = attributes.item(i);
            finalDefinition = decorateIfRequired(node, finalDefinition, containingBd);
        }

        // 遍历所有的子标签，看是否有适用于修饰的子标签
        NodeList children = ele.getChildNodes();
        for (int i = 0; i < children.getLength(); i++) {
            Node node = children.item(i);
            if (node.getNodeType() == Node.ELEMENT_NODE) {
                finalDefinition = decorateIfRequired(node, finalDefinition, containingBd);
            }
        }
        return finalDefinition;
    }

    public BeanDefinitionHolder decorateIfRequired(
            Node node, BeanDefinitionHolder originalDef, @Nullable BeanDefinition containingBd) {
        // 获取自定义标签的命名空间
        String namespaceUri = getNamespaceURI(node);
        // 要修饰非默认标签
        if (namespaceUri != null && !isDefaultNamespace(namespaceUri)) {
            // 根据命名空间找到对应的处理器
            NamespaceHandler handler = this.readerContext.getNamespaceHandlerResolver().resolve(namespaceUri);
            if (handler != null) {
                // 进行修饰
                BeanDefinitionHolder decorated =
                        handler.decorate(node, originalDef, new ParserContext(this.readerContext, this, containingBd));
                if (decorated != null) {
                    return decorated;
                }
            }
            else if (namespaceUri.startsWith("http://www.springframework.org/")) {
                error("Unable to locate Spring NamespaceHandler for XML schema namespace [" + namespaceUri + "]", node);
            }
        }
        return originalDef;
    }
}
```
