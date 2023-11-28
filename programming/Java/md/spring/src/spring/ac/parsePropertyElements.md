# 解析 property 子标签

```java
public class BeanDefinitionParserDelegate {

    public void parsePropertyElements(Element beanEle, BeanDefinition bd) {
        NodeList nl = beanEle.getChildNodes();
        for (int i = 0; i < nl.getLength(); i++) {
            Node node = nl.item(i);
            if (isCandidateElement(node) && nodeNameEquals(node, PROPERTY_ELEMENT)) {
                // 解析property标签
                parsePropertyElement((Element) node, bd);
            }
        }
    }

    public void parsePropertyElement(Element ele, BeanDefinition bd) {
        String propertyName = ele.getAttribute(NAME_ATTRIBUTE);
        if (!StringUtils.hasLength(propertyName)) {
            error("Tag 'property' must have a 'name' attribute", ele);
            return;
        }
        this.parseState.push(new PropertyEntry(propertyName));
        try {
            if (bd.getPropertyValues().contains(propertyName)) {
                // property的name重复
                error("Multiple 'property' definitions for property '" + propertyName + "'", ele);
                return;
            }
            // 解析property的值, 和解析constructor-arg的值用的一个方法
            Object val = parsePropertyValue(ele, bd, propertyName);
            PropertyValue pv = new PropertyValue(propertyName, val);
            parseMetaElements(ele, pv);
            pv.setSource(extractSource(ele));
            // 添加到BeanDefinition的propertyValueList中
            bd.getPropertyValues().addPropertyValue(pv);
        }
        finally {
            this.parseState.pop();
        }
    }
}
```
