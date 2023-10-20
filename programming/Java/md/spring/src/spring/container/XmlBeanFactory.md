# XmlBeanFactory

当通过Resource相关类完成了对配置文件进行封装后，配置文件的读取工作就会交给XmlBeanFactory来处理：

1. 关闭部分接口的自动装配功能
2. 加载BeanDefinition

```java
public class XmlBeanFactory extends DefaultListableBeanFactory {
    private final XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(this);

    // 使用Resource实例作为参数的构造方法
    public XmlBeanFactory(Resource resource) throws BeansException {
        this(resource, null);
    }

    public XmlBeanFactory(Resource resource, BeanFactory parentBeanFactory) throws BeansException {
        // 关闭给定接口的自动装配功能
        super(parentBeanFactory);
        // 加载BeanDefinition
        this.reader.loadBeanDefinitions(resource);
    }
}
```

## 关闭给定接口的自动装配功能

```java
// XmlBeanFactory的祖先类
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {

    // super(parentBeanFactory)会调用到这里
    public AbstractAutowireCapableBeanFactory(@Nullable BeanFactory parentBeanFactory) {
        this();
        setParentBeanFactory(parentBeanFactory);
    }

    public AbstractAutowireCapableBeanFactory() {
        super();
        // 关闭这些接口的自动装配功能
        ignoreDependencyInterface(BeanNameAware.class);
        ignoreDependencyInterface(BeanFactoryAware.class);
        ignoreDependencyInterface(BeanClassLoaderAware.class);
    }
}
```

## 加载BeanDefinition

BeanDefinition就是bean在Spring中的内部表示形式。

加载BeanDefinition的过程：

1. 解析xml配置文件
2. 注册BeanDefinition

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    // 用于记录正在加载的xml配置文件
    private final ThreadLocal<Set<EncodedResource>> resourcesCurrentlyBeingLoaded =
            new NamedThreadLocal<>("XML bean definition resources currently being loaded");

    // 加载BeanDefinition
    public int loadBeanDefinitions(Resource resource) throws BeanDefinitionStoreException {
        // 封装xml配置文件
        // EncodedResource在设置了编码属性的时候，会使用指定编码读取资源文件
        return loadBeanDefinitions(new EncodedResource(resource));
    }

    public int loadBeanDefinitions(EncodedResource encodedResource)
            throws BeanDefinitionStoreException {
        // 看一下有没有正在加载的xml配置文件
        Set<EncodedResource> currentResources = this.resourcesCurrentlyBeingLoaded.get();
        if (currentResources == null) {
            // 第一次加载，初始化resourcesCurrentlyBeingLoaded
            currentResources = new HashSet<>(4);
            this.resourcesCurrentlyBeingLoaded.set(currentResources);
        }

        // 添加当前xml配置文件
        if (!currentResources.add(encodedResource)) {
            // 添加失败
            throw new BeanDefinitionStoreException(
                    "Detected cyclic loading of " + encodedResource + " - check your import definitions!");
        }

        try {
            // 获取xml配置文件的InpurStream
            InputStream inputStream = encodedResource.getResource().getInputStream();
            try {
                // 由于使用了SAX来读取XML文件
                // 所以需要把InputStream封装成SAX要求的参数类型InputSource
                InputSource inputSource = new InputSource(inputStream);
                if (encodedResource.getEncoding() != null) {
                    inputSource.setEncoding(encodedResource.getEncoding());
                }
                // 加载BeanDefinition
                return doLoadBeanDefinitions(inputSource, encodedResource.getResource());
            } finally {
                inputStream.close();
            }
        } catch (IOException ex) {
            throw new BeanDefinitionStoreException(
                    "IOException parsing XML document from " + encodedResource.getResource(), ex);
        } finally {
            // 加载完了，从resourcesCurrentlyBeingLoaded中移除这个xml文件
            currentResources.remove(encodedResource);
            if (currentResources.isEmpty()) {
                this.resourcesCurrentlyBeingLoaded.remove();
            }
        }
    }

    // 加载BeanDefinition
    protected int doLoadBeanDefinitions(InputSource inputSource, Resource resource)
            throws BeanDefinitionStoreException {
        try {
            // 解析XML
            Document doc = doLoadDocument(inputSource, resource);
            // 注册BeanDefinition
            return registerBeanDefinitions(doc, resource);
        }
        catch (BeanDefinitionStoreException ex) {
            // ...
        }
    }
}
```
