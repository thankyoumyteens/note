# XML的验证模式

XML文件的验证模式保证了XML文件的正确性，其中，DTD（Document Type Definition）和XSD（XML Schema Definition）是最常用的两种模式。

## DTD

文档类型定义(Document Type Definition，DTD)是一种特殊类型的文件，可以通过比较XML文档和DTD文件来看文档是否符合规范，元素和标签使用是否正确。一个DTD文档包含：元素的定义规则，元素间关系的定义规则，元素可使用的属性，可使用的实体或符号规则。

## XSD

XML结构定义(XML Schema Definition，XSD)描述了XML文档的结构。可以用一个指定的XML Schema来验证某个XML文档， 以检查该XML文档是否符合其要求。XML Schema本身也是XML文档，它符合XML语法结构，可以用通用的XML解析器解析它。

## 获取XML的验证模式

Spring通过getValidationModeForResource()方法获取XML文件的验证模式。

> spring-framework-5.0.x\spring-beans\src\main\java\org\springframework\beans\factory\xml\XmlBeanDefinitionReader.java

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    protected int getValidationModeForResource(Resource resource) {
        int validationModeToUse = getValidationMode();
        // 可以通过XmlBeanDefinitionReader::setValidationMode()方法手动指定验证模式
        // 如果手动指定了验证模式则使用指定的验证模式
        if (validationModeToUse != VALIDATION_AUTO) {
            return validationModeToUse;
        }
        // 自动检测
        int detectedMode = detectValidationMode(resource);
        if (detectedMode != VALIDATION_AUTO) {
            return detectedMode;
        }
        return VALIDATION_XSD;
    }

    public int getValidationMode() {
        return this.validationMode;
    }

    // 自动检测
    protected int detectValidationMode(Resource resource) {
        if (resource.isOpen()) {
            throw new BeanDefinitionStoreException(
                    "Passed-in Resource [" + resource + "] contains an open stream: " +
                    "cannot determine validation mode automatically. Either pass in a Resource " +
                    "that is able to create fresh streams, or explicitly specify the validationMode " +
                    "on your XmlBeanDefinitionReader instance.");
        }

        InputStream inputStream;
        try {
            inputStream = resource.getInputStream();
        }
        catch (IOException ex) {
            throw new BeanDefinitionStoreException(
                    "Unable to determine validation mode for [" + resource + "]: cannot open InputStream. " +
                    "Did you attempt to load directly from a SAX InputSource without specifying the " +
                    "validationMode on your XmlBeanDefinitionReader instance?", ex);
        }

        try {
            return this.validationModeDetector.detectValidationMode(inputStream);
        }
        catch (IOException ex) {
            throw new BeanDefinitionStoreException("Unable to determine validation mode for [" +
                    resource + "]: an error occurred whilst reading from the InputStream.", ex);
        }
    }
}
```

detectValidationMode()方法中调用了XmlValidationModeDetector::detectValidationMode()方法检测XML验证模式：

> spring-framework-5.0.x\spring-core\src\main\java\org\springframework\util\xml\XmlValidationModeDetector.java

```java
public class XmlValidationModeDetector {

    private static final String DOCTYPE = "DOCTYPE";

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
        }
        catch (CharConversionException ex) {
            return VALIDATION_AUTO;
        }
        finally {
            reader.close();
        }
    }

    private boolean hasDoctype(String content) {
        return content.contains(DOCTYPE);
    }
}
```

Spring 用来检测验证模式的办法就是判断XML文件里是否包含DOCTYPE，如果包含就是DTD，否则就是XSD。
