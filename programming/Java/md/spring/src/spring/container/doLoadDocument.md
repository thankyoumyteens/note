# doLoadDocument

解析xml配置文件的过程：

1. 获取XML文件的验证模式
2. 使用这个验证模式解析XML文件

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    // 解析XML
    protected Document doLoadDocument(InputSource inputSource, Resource resource) 
            throws Exception {
        // getValidationModeForResource()方法获取XML文件的验证模式
        // getEntityResolver()方法返回一个EntityResolver对象，
        // EntityResolver用来读取本地的DTD/XSD文件并返回给SAX，避免了去网络上寻找相应的声明
        // loadDocument()方法解析XML文件
        return this.documentLoader.loadDocument(inputSource, getEntityResolver(), 
            this.errorHandler, getValidationModeForResource(resource), isNamespaceAware());
    }
}
```

## XML的验证模式

XML文件的验证模式保证了XML文件的正确性，其中，DTD（Document Type Definition）和XSD（XML Schema Definition）是最常用的两种模式。

- DTD：文档类型定义(Document Type Definition，DTD)是一种特殊类型的文件，可以通过比较XML文档和DTD文件来看文档是否符合规范，元素和标签使用是否正确。一个DTD文档包含：元素的定义规则，元素间关系的定义规则，元素可使用的属性，可使用的实体或符号规则
- XSD：XML结构定义(XML Schema Definition，XSD)描述了XML文档的结构。可以用一个指定的XML Schema来验证某个XML文档， 以检查该XML文档是否符合其要求。XML Schema本身也是XML文档，它符合XML语法结构，可以用通用的XML解析器解析它

## 获取XML的验证模式

获取XML的验证模式的过程：

1. 如果用户手动指定了验证模式，则使用用户指定的验证模式
2. 如果用户没有指定，则自动检测xml文件使用的验证模式

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
        // 没检测出来，使用XSD模式
        return VALIDATION_XSD;
    }

    // 自动检测验证模式
    protected int detectValidationMode(Resource resource) {
        if (resource.isOpen()) {
            throw new BeanDefinitionStoreException(
                    "Passed-in Resource [" + resource + "] contains an open stream: " +
                    "cannot determine validation mode automatically. Either pass in a Resource " +
                    "that is able to create fresh streams, or explicitly specify the validationMode " +
                    "on your XmlBeanDefinitionReader instance.");
        }

        // 获取xml配置文件的InpurStream
        InputStream inputStream;
        try {
            inputStream = resource.getInputStream();
        } catch (IOException ex) {
            throw new BeanDefinitionStoreException(
                    "Unable to determine validation mode for [" + resource + "]: cannot open InputStream. " +
                    "Did you attempt to load directly from a SAX InputSource without specifying the " +
                    "validationMode on your XmlBeanDefinitionReader instance?", ex);
        }

        try {
            // 检测XML验证模式
            return this.validationModeDetector.detectValidationMode(inputStream);
        } catch (IOException ex) {
            throw new BeanDefinitionStoreException("Unable to determine validation mode for [" +
                    resource + "]: an error occurred whilst reading from the InputStream.", ex);
        }
    }
}
```

## 检测XML验证模式

检测XML验证模式的过程：

1. 检测XML配置文件中是否含有字符串：DOCTYPE
2. 如果有，则验证模式为DTD
3. 如果没有，则验证模式为XSD

```java
public class XmlValidationModeDetector {

    // 检测XML验证模式
    public int detectValidationMode(InputStream inputStream) throws IOException {
        // 检测用户的XML配置文件中是否含有 DOCTYPE
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
                // 已经读取到的xml的正文内容了，后面不会再有验证文件的声明
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
        // private static final String DOCTYPE = "DOCTYPE";
        return content.contains(DOCTYPE);
    }
}
```

## 解析XML配置文件

使用SAX解析XML，并返回Document对象：

```java
public class DefaultDocumentLoader implements DocumentLoader {

    // 解析XML文件
    public Document loadDocument(InputSource inputSource, EntityResolver entityResolver, ErrorHandler errorHandler, int validationMode, boolean namespaceAware) 
                throws Exception {
        // 通过SAX解析XML文档的固定操作
        DocumentBuilderFactory factory = createDocumentBuilderFactory(validationMode, namespaceAware);
        DocumentBuilder builder = createDocumentBuilder(factory, entityResolver, errorHandler);
        return builder.parse(inputSource);
    }
}
```
