# 创建 BeanDefinition

```java
public class BeanDefinitionParserDelegate {

    protected AbstractBeanDefinition createBeanDefinition(@Nullable String className, 
                                                          @Nullable String parentName)
            throws ClassNotFoundException {
        // 创建BeanDefinition
        return BeanDefinitionReaderUtils.createBeanDefinition(parentName,
                className, this.readerContext.getBeanClassLoader());
    }
}

public class BeanDefinitionReaderUtils {

    public static AbstractBeanDefinition createBeanDefinition(
            @Nullable String parentName, @Nullable String className, @Nullable ClassLoader classLoader) throws ClassNotFoundException {

        GenericBeanDefinition bd = new GenericBeanDefinition();
        bd.setParentName(parentName);
        if (className != null) {
            if (classLoader != null) {
                // 如果classLoader不为空, 则使用以传入的classLoader
                // 把bean的class属性设置的类加载进jvm
                bd.setBeanClass(ClassUtils.forName(className, classLoader));
            } else {
                // 没传classLoader的话, 就只把类的全名记录到BeanDefinition中
                bd.setBeanClassName(className);
            }
        }
        return bd;
    }
}
```
