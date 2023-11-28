# 解析 replaced-method 子标签

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
                // 如果有参数, 就记录参数
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
