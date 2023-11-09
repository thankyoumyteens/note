# 加载 BeanDefinition

```java
public class XmlBeanDefinitionReader extends AbstractBeanDefinitionReader {

    // 用于记录正在加载的资源(xml配置文件的Resource)
    private final ThreadLocal<Set<EncodedResource>> resourcesCurrentlyBeingLoaded =
            new NamedThreadLocal<>("XML bean definition resources currently being loaded");

    /**
     * 加载BeanDefinition
     * 
     * @param resource xml配置文件的Resource
     */
    public int loadBeanDefinitions(Resource resource) throws BeanDefinitionStoreException {
        // 封装resource
        // EncodedResource用于使用指定编码读取xml文件
        return loadBeanDefinitions(new EncodedResource(resource));
    }

    public int loadBeanDefinitions(EncodedResource encodedResource)
            throws BeanDefinitionStoreException {
        // 看一下有没有正在加载的资源
        Set<EncodedResource> currentResources = this.resourcesCurrentlyBeingLoaded.get();
        if (currentResources == null) {
            // 第一次加载，初始化resourcesCurrentlyBeingLoaded
            currentResources = new HashSet<>(4);
            this.resourcesCurrentlyBeingLoaded.set(currentResources);
        }

        // 添加当前资源
        if (!currentResources.add(encodedResource)) {
            // 资源正在被加载，抛出异常
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
            // 加载完了，从resourcesCurrentlyBeingLoaded中移除这个资源
            currentResources.remove(encodedResource);
            if (currentResources.isEmpty()) {
                this.resourcesCurrentlyBeingLoaded.remove();
            }
        }
    }

    /**
     * 加载BeanDefinition
     */
    protected int doLoadBeanDefinitions(InputSource inputSource, Resource resource)
            throws BeanDefinitionStoreException {
        try {
            // 解析xml
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
