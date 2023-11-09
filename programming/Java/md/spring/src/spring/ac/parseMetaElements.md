# 解析 meta 子标签

meta 标签是一个额外的声明，当需要使用里面的信息的时候可以通过 BeanDefinition 的 getAttribute(key)方法进行获取。

```xml
<bean id="myTestBean" class="bean.MyTestBean">
  <meta key="test" value="testVal"/>
</bean>
```

解析 meta 标签，并存储到 BeanDefinition 中。

```java
public class BeanDefinitionParserDelegate {

    public void parseMetaElements(Element ele, BeanMetadataAttributeAccessor attributeAccessor) {
        // 获取当前节点的所有子节点
        NodeList nl = ele.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            // 解析meta标签
            if (isCandidateElement(node) && nodeNameEquals(node, META_ELEMENT)) {
                Element metaElement = (Element) node;
                // 读取meta标签的key和value，并存储到BeanDefinition中
                String key = metaElement.getAttribute(KEY_ATTRIBUTE);
                String value = metaElement.getAttribute(VALUE_ATTRIBUTE);
                BeanMetadataAttribute attribute = new BeanMetadataAttribute(key, value);
                attribute.setSource(extractSource(metaElement));
                // AbstractBeanDefinition继承了BeanMetadataAttributeAccessor
                attributeAccessor.addMetadataAttribute(attribute);
            }
        }
    }
}
```
