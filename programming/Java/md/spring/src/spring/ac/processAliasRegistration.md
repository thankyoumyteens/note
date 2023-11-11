# 解析 alias 标签

spring 中声明别名的方式：

1. 通过 bean 的 name 属性：

```xml
<bean id="user" name="user1,user2" class="com.pojo.User"/>
```

2. 通过 alias 标签：

```xml
<bean id="user" class="com.pojo.User"/>
<alias name="user" alias="user1,user2"/>
```

解析 alias 标签：

```java
public class DefaultBeanDefinitionDocumentReader implements BeanDefinitionDocumentReader {

    protected void processAliasRegistration(Element ele) {
        // 获取beanName
        String name = ele.getAttribute(NAME_ATTRIBUTE);
        // 获取别名
        String alias = ele.getAttribute(ALIAS_ATTRIBUTE);
        boolean valid = true;
        if (!StringUtils.hasText(name)) {
            getReaderContext().error("Name must not be empty", ele);
            valid = false;
        }
        if (!StringUtils.hasText(alias)) {
            getReaderContext().error("Alias must not be empty", ele);
            valid = false;
        }
        if (valid) {
            try {
                // 注册别名
                getReaderContext().getRegistry().registerAlias(name, alias);
            }
            catch (Exception ex) {
                getReaderContext().error("Failed to register alias '" + alias +
                        "' for bean with name '" + name + "'", ele, ex);
            }
            // 通知相关的监听器，这个alias已经注册完成了
            getReaderContext().fireAliasRegistered(name, alias, extractSource(ele));
        }
    }
}
```
