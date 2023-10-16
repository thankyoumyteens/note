# XmlBeanFactory

当通过Resource相关类完成了对配置文件进行封装后，配置文件的读取工作就会交给XmlBeanFactory来处理。

```java
BeanFactory bf = new XmlBeanFactory(resource);
```

使用Resource实例作为参数的构造方法：

```java
public class XmlBeanFactory extends DefaultListableBeanFactory {
    private final XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(this);

    public XmlBeanFactory(Resource resource) throws BeansException {
        // 调用另一个构造方法
        this(resource, null);
    }

    public XmlBeanFactory(Resource resource, BeanFactory parentBeanFactory) throws BeansException {
        super(parentBeanFactory);
        // 加载资源
        this.reader.loadBeanDefinitions(resource);
    }
}
```
