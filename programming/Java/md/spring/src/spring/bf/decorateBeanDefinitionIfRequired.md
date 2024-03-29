# 解析 bean 标签下的自定义子标签

bean 标签下的自定义标签是一种装饰器模式。装饰器模式的作用是对对象已有的功能进行增强，但是不改变原有对象结构。这避免了通过继承方式进行功能扩充导致的类体系臃肿。

```xml
<bean id="testBean" class="test.TestBean">
  <mybean:user username="123"/>
</bean>
```

bean 标签下的自定义标签会委托给 BeanDefinitionParserDelegate::decorateBeanDefinitionIfRequired()方法解析。

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

        // 遍历所有的属性，看是否有适用于装饰的自定义属性
        NamedNodeMap attributes = ele.getAttributes();
        for (int i = 0; i < attributes.getLength(); i++) {
            Node node = attributes.item(i);
            finalDefinition = decorateIfRequired(node, finalDefinition, containingBd);
        }

        // 遍历所有的子标签，看是否有适用于装饰的自定义标签
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
        if (namespaceUri != null && !isDefaultNamespace(namespaceUri)) {
            // 根据命名空间找到对应的处理器
            NamespaceHandler handler = this.readerContext.getNamespaceHandlerResolver().resolve(namespaceUri);
            if (handler != null) {
                // 进行装饰，decorate()方法由用户重写
                BeanDefinitionHolder decorated =
                        handler.decorate(node, originalDef, new ParserContext(this.readerContext, this, containingBd));
                if (decorated != null) {
                    return decorated;
                }
            } else if (namespaceUri.startsWith("http://www.springframework.org/")) {
                error("Unable to locate Spring NamespaceHandler for XML schema namespace [" + namespaceUri + "]", node);
            }
        }
        return originalDef;
    }
}
```
