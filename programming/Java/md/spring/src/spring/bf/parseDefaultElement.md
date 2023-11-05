# parseDefaultElement

解析默认命名空间的标签分为以下几种情况：

1. 解析import标签
2. 解析alias标签
3. 解析bean标签
4. 解析beans标签

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    private void parseDefaultElement(Element ele, BeanDefinitionParserDelegate delegate) {
        if (delegate.nodeNameEquals(ele, IMPORT_ELEMENT)) {
            // 解析import标签
            importBeanDefinitionResource(ele);
        } else if (delegate.nodeNameEquals(ele, ALIAS_ELEMENT)) {
            // 解析alias标签
            processAliasRegistration(ele);
        } else if (delegate.nodeNameEquals(ele, BEAN_ELEMENT)) {
            // 解析bean标签
            processBeanDefinition(ele, delegate);
        } else if (delegate.nodeNameEquals(ele, NESTED_BEANS_ELEMENT)) {
            // 解析beans标签
            // 递归去调用DefaultBeanDefinitionDocumentReader::doRegisterBeanDefinitions()
            doRegisterBeanDefinitions(ele);
        }
    }
}
```
