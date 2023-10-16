# 解析XML配置文件

XmlBeanDefinitionReader中通过loadDocument()方法解析XML文件：

> spring-framework-5.0.x\spring-beans\src\main\java\org\springframework\beans\factory\xml\DefaultDocumentLoader.java

```java
public class DefaultDocumentLoader implements DocumentLoader {

    // 解析XML文件
    public Document loadDocument(InputSource inputSource, EntityResolver entityResolver,
            ErrorHandler errorHandler, int validationMode, boolean namespaceAware) 
                throws Exception {
        // 通过SAX解析XML文档的固定操作
        DocumentBuilderFactory factory = createDocumentBuilderFactory(validationMode, namespaceAware);
        DocumentBuilder builder = createDocumentBuilder(factory, entityResolver, errorHandler);
        return builder.parse(inputSource);
    }
}
```
