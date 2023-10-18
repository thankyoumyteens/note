# createBeanDefinition

BeanDefinition是一个接口，是bean标签在Spring容器中的内部表示形式。

- AbstractBeanDefinition：内部默认实现了BeanDefinition的绝大部分方法，对一些属性进行了默认值的赋值，其他的实现类基本上都是在AbstractBeanDefinition的基础上完成的
- RootBeanDefinition：它对应一般的bean标签
- ChildBeanDefinition：在配置文件中可以定义父bean标签和子bean标签，父bean用RootBeanDefinition表示，而子bean用ChildBeanDefinition表示，而没有父bean的bean标签就使用RootBeanDefinition表示
- GenericBeanDefinition：Spring2.5以后新加入的BeanDefinition实现类，同时兼具RootBeanDefinition和ChildBeanDefinition的功能，自从有了GenericBeanDefinition之后，RootBeanDefinition和ChildBeanDefinition相对就用的少了

createBeanDefinition()方法会创建一个GenericBeanDefinition的对象并返回。

```java
public class BeanDefinitionParserDelegate {

    protected AbstractBeanDefinition createBeanDefinition(@Nullable String className, @Nullable String parentName)
            throws ClassNotFoundException {

        return BeanDefinitionReaderUtils.createBeanDefinition(
                parentName, className, this.readerContext.getBeanClassLoader());
    }
}

public class BeanDefinitionReaderUtils {

    public static AbstractBeanDefinition createBeanDefinition(
            @Nullable String parentName, @Nullable String className, @Nullable ClassLoader classLoader) throws ClassNotFoundException {

        GenericBeanDefinition bd = new GenericBeanDefinition();
        bd.setParentName(parentName);
        if (className != null) {
            if (classLoader != null) {
                // 如果classLoader不为空，则使用以传人的classLoader加载类
                bd.setBeanClass(ClassUtils.forName(className, classLoader));
            }
            else {
                // 否则只是记录className
                bd.setBeanClassName(className);
            }
        }
        return bd;
    }
}
```
