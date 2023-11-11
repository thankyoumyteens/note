# 解析 import 标签

import 标签用于导入其它配置文件。为了避免一个配置文件内容过多，可以将一个配置文件根据业务进行拆分，拆分后的配置文件使用 import 标签导入到主配置文件中，项目加载主配置文件就可以把 import 导入的文件一起加载。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--导入模块A的配置文件-->
    <import resource="moduleAContext.xml"/>

    <!--导入模块B的配置文件-->
    <import resource="moduleBContext.xml"/>
</beans>
```

解析 import 标签：

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    protected void importBeanDefinitionResource(Element ele) {
        // 获取resource属性
        String location = ele.getAttribute(RESOURCE_ATTRIBUTE);
        if (!StringUtils.hasText(location)) {
            getReaderContext().error("Resource location must not be empty", ele);
            return;
        }

        // 解析系统属性，比如："${user.dir}"
        location = getReaderContext().getEnvironment().resolveRequiredPlaceholders(location);

        Set<Resource> actualResources = new LinkedHashSet<>(4);

        // 是否使用绝对路径
        boolean absoluteLocation = false;
        try {
            absoluteLocation = ResourcePatternUtils.isUrl(location) || ResourceUtils.toURI(location).isAbsolute();
        } catch (URISyntaxException ex) {}

        if (absoluteLocation) {
            try {
                // 使用绝对路径解析xml
                // 与XmlBeanFactory()一样，
                // 调用AbstractBeanDefinitionReader::loadBeanDefinitions()
                // 去加载BeanDefinition：
                // 1. 解析xml配置文件
                // 2. 注册BeanDefinition
                int importCount = getReaderContext().getReader().loadBeanDefinitions(location, actualResources);
            } catch (BeanDefinitionStoreException ex) {
                getReaderContext().error(
                        "Failed to import bean definitions from URL location [" + location + "]", ele, ex);
            }
        } else {
            try {
                // 使用相对路径解析xml
                int importCount;
                Resource relativeResource = getReaderContext().getResource().createRelative(location);
                if (relativeResource.exists()) {
                    // 加载BeanDefinition
                    importCount = getReaderContext().getReader().loadBeanDefinitions(relativeResource);
                    actualResources.add(relativeResource);
                } else {
                    String baseLocation = getReaderContext().getResource().getURL().toString();
                    // 加载BeanDefinition
                    importCount = getReaderContext().getReader().loadBeanDefinitions(
                            StringUtils.applyRelativePath(baseLocation, location), actualResources);
                }
            } catch (IOException ex) {
                // ...
            }
        }
        Resource[] actResArray = actualResources.toArray(new Resource[0]);
        // 通知相关的监听器
        getReaderContext().fireImportProcessed(location, actResArray, extractSource(ele));
    }
}
```
