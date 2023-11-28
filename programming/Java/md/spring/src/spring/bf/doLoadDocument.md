# doLoadDocument

解析 xml 配置文件的过程: 

1. 获取 XML 文件的验证模式
2. 使用这个验证模式解析 XML 文件

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    // 解析XML
    protected Document doLoadDocument(InputSource inputSource, Resource resource)
            throws Exception {
        // getValidationModeForResource()方法获取XML文件的验证模式
        // getEntityResolver()方法返回一个EntityResolver对象, 
        // EntityResolver用来读取本地的DTD/XSD文件并返回给SAX, 避免了去网络上寻找相应的声明
        // loadDocument()方法解析XML文件
        return this.documentLoader.loadDocument(inputSource, getEntityResolver(),
            this.errorHandler, getValidationModeForResource(resource), isNamespaceAware());
    }
}
```

## XML 的验证模式

XML 文件的验证模式保证了 XML 文件的正确性, 其中, DTD（Document Type Definition）和 XSD（XML Schema Definition）是最常用的两种模式。

- DTD: 文档类型定义(Document Type Definition, DTD)是一种特殊类型的文件, 可以通过比较 XML 文档和 DTD 文件来看文档是否符合规范, 元素和标签使用是否正确。一个 DTD 文档包含: 元素的定义规则, 元素间关系的定义规则, 元素可使用的属性, 可使用的实体或符号规则
- XSD: XML 结构定义(XML Schema Definition, XSD)描述了 XML 文档的结构。可以用一个指定的 XML Schema 来验证某个 XML 文档,  以检查该 XML 文档是否符合其要求。XML Schema 本身也是 XML 文档, 它符合 XML 语法结构, 可以用通用的 XML 解析器解析它

## 获取 XML 的验证模式

获取 XML 的验证模式的过程: 

1. 如果用户手动指定了验证模式, 则使用用户指定的验证模式
2. 如果用户没有指定, 则自动检测 xml 文件使用的验证模式

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    protected int getValidationModeForResource(Resource resource) {
        // 获取用户指定的验证模式
        // 可以通过XmlBeanDefinitionReader::setValidationMode()方法手动指定验证模式
        int validationModeToUse = getValidationMode();
        if (validationModeToUse != VALIDATION_AUTO) {
            // 如果手动指定了验证模式则使用指定的验证模式
            return validationModeToUse;
        }
        // 自动检测验证模式
        int detectedMode = detectValidationMode(resource);
        if (detectedMode != VALIDATION_AUTO) {
            return detectedMode;
        }
        // 没检测出来, 使用XSD模式
        return VALIDATION_XSD;
    }

    /**
     * 自动检测验证模式
     */
    protected int detectValidationMode(Resource resource) {
        // ...
        // 获取xml配置文件的InpurStream
        InputStream inputStream;
        try {
            inputStream = resource.getInputStream();
        } catch (IOException ex) {
            // ...
        }

        try {
            // 检测XML验证模式
            return this.validationModeDetector.detectValidationMode(inputStream);
        } catch (IOException ex) {
            // ...
        }
    }
}
```

## 检测 XML 验证模式

检测 XML 验证模式的过程: 

1. 检测 XML 配置文件中是否含有字符串: DOCTYPE
2. 如果有, 则验证模式为 DTD
3. 如果没有, 则验证模式为 XSD

```java
public class XmlValidationModeDetector {

    public int detectValidationMode(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        try {
            boolean isDtdValidated = false;
            String content;
            while ((content = reader.readLine()) != null) {
                content = consumeCommentTokens(content);
                // 跳过注释
                if (this.inComment || !StringUtils.hasText(content)) {
                    continue;
                }
                // XML文件中是否含有字符串"DOCTYPE"
                if (hasDoctype(content)) {
                    // 使用DTD验证XML文件
                    isDtdValidated = true;
                    break;
                }
                // 已经读取到的xml的正文内容了, 后面不会再有验证文件的声明
                if (hasOpeningTag(content)) {
                    break;
                }
            }
            return (isDtdValidated ? VALIDATION_DTD : VALIDATION_XSD);
        } catch (CharConversionException ex) {
            // 没检测出来
            return VALIDATION_AUTO;
        } finally {
            reader.close();
        }
    }

    private boolean hasDoctype(String content) {
        // DOCTYPE的值: "DOCTYPE"
        return content.contains(DOCTYPE);
    }
}
```

## 解析 XML 配置文件

使用 SAX 解析 XML, 并返回 Document 对象: 

```java
public class DefaultDocumentLoader implements DocumentLoader {

    public Document loadDocument(InputSource inputSource, EntityResolver entityResolver, ErrorHandler errorHandler, int validationMode, boolean namespaceAware)
                throws Exception {
        // 通过SAX解析XML文档的固定操作
        DocumentBuilderFactory factory = createDocumentBuilderFactory(validationMode, namespaceAware);
        DocumentBuilder builder = createDocumentBuilder(factory, entityResolver, errorHandler);
        return builder.parse(inputSource);
    }
}
```
