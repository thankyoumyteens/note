# 解析 qualifier 子标签

qualifier 用于在有多个相同类型 bean 的时候指定 bean 的名称以消除歧义：

```java
@Autowired
@Qualifier("obj1")
private MyObj obj2;

@Autowired
@Qualifier("obj2")
private MyObj obj2;
```

parseQualifierElements()方法会解析 bean 的 qualifier 子标签。

```java
public class BeanDefinitionParserDelegate {

    public void parseQualifierElements(Element beanEle, AbstractBeanDefinition bd) {
        NodeList nl = beanEle.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            if (isCandidateElement(node) && nodeNameEquals(node, QUALIFIER_ELEMENT)) {
                parseQualifierElement((Element) node, bd);
            }
        }
    }

    public void parseQualifierElement(Element ele, AbstractBeanDefinition bd) {
        String typeName = ele.getAttribute(TYPE_ATTRIBUTE);
        if (!StringUtils.hasLength(typeName)) {
            error("Tag 'qualifier' must have a 'type' attribute", ele);
            return;
        }
        this.parseState.push(new QualifierEntry(typeName));
        try {
            AutowireCandidateQualifier qualifier = new AutowireCandidateQualifier(typeName);
            qualifier.setSource(extractSource(ele));
            String value = ele.getAttribute(VALUE_ATTRIBUTE);
            if (StringUtils.hasLength(value)) {
                qualifier.setAttribute(AutowireCandidateQualifier.VALUE_KEY, value);
            }
            NodeList nl = ele.getChildNodes();
            for (int i = 0; i < nl.getLength(); i++) {
                Node node = nl.item(i);
                if (isCandidateElement(node) && nodeNameEquals(node, QUALIFIER_ATTRIBUTE_ELEMENT)) {
                    Element attributeEle = (Element) node;
                    String attributeName = attributeEle.getAttribute(KEY_ATTRIBUTE);
                    String attributeValue = attributeEle.getAttribute(VALUE_ATTRIBUTE);
                    if (StringUtils.hasLength(attributeName) && StringUtils.hasLength(attributeValue)) {
                        BeanMetadataAttribute attribute = new BeanMetadataAttribute(attributeName, attributeValue);
                        attribute.setSource(extractSource(attributeEle));
                        qualifier.addMetadataAttribute(attribute);
                    }
                    else {
                        error("Qualifier 'attribute' tag must have a 'name' and 'value'", attributeEle);
                        return;
                    }
                }
            }
            bd.addQualifier(qualifier);
        }
        finally {
            this.parseState.pop();
        }
    }
}
```
