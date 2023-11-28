# 创建 BeanFactory

```java
public abstract class AbstractApplicationContext extends DefaultResourceLoader
        implements ConfigurableApplicationContext {

    protected ConfigurableListableBeanFactory obtainFreshBeanFactory() {
        // 初始化BeanFactory, 并加载BeanDefinition
        refreshBeanFactory();
        // 返回BeanFactory对象
        ConfigurableListableBeanFactory beanFactory = getBeanFactory();
        return beanFactory;
    }
}

public abstract class AbstractRefreshableApplicationContext extends AbstractApplicationContext {

    private volatile DefaultListableBeanFactory beanFactory;

    /**
     * 创建BeanFactory, 并存储到当前ApplicationContext对象的字段中
     */
    protected final void refreshBeanFactory() throws BeansException {
        if (hasBeanFactory()) {
            destroyBeans();
            closeBeanFactory();
        }
        try {
            // 创建一个BeanFactory对象
            DefaultListableBeanFactory beanFactory = createBeanFactory();
            // 允许BeanFactory根据这个getId()返回的id反序列化出来
            beanFactory.setSerializationId(getId());
            // 定制BeanFactory
            customizeBeanFactory(beanFactory);
            // 创建BeanDefinitionReader, 并加载BeanDefinition
            loadBeanDefinitions(beanFactory);
            this.beanFactory = beanFactory;
        } catch (IOException ex) {
            throw new ApplicationContextException("I/O error parsing bean definition source for " + getDisplayName(), ex);
        }
    }

    /**
     * 定制BeanFactory
     */
    protected void customizeBeanFactory(DefaultListableBeanFactory beanFactory) {
        // 把ApplicationContext的设置同步到BeanFactory中
        // 配置是否允许覆盖同名称的不同定义的对象
        if (this.allowBeanDefinitionOverriding != null) {
            beanFactory.setAllowBeanDefinitionOverriding(this.allowBeanDefinitionOverriding);
        }
        // 配置是否允许 bean 之间存在循环依赖
        if (this.allowCircularReferences != null) {
            beanFactory.setAllowCircularReferences(this.allowCircularReferences);
        }
    }
}

public abstract class AbstractXmlApplicationContext extends AbstractRefreshableConfigApplicationContext {

    protected void loadBeanDefinitions(DefaultListableBeanFactory beanFactory) throws BeansException, IOException {
        // 创建XmlBeanDefinitionReader用来解析xml配置文件
        XmlBeanDefinitionReader beanDefinitionReader = new XmlBeanDefinitionReader(beanFactory);

        // 给XmlBeanDefinitionReader配置环境变量
        beanDefinitionReader.setEnvironment(this.getEnvironment());
        beanDefinitionReader.setResourceLoader(this);
        beanDefinitionReader.setEntityResolver(new ResourceEntityResolver(this));

        // 允许子类自定义beanDefinitionReader的初始化操作
        initBeanDefinitionReader(beanDefinitionReader);
        // 加载BeanDefinition
        loadBeanDefinitions(beanDefinitionReader);
    }

    /**
     * 加载BeanDefinition
     */
    protected void loadBeanDefinitions(XmlBeanDefinitionReader reader) throws BeansException, IOException {
        // 获取xml配置文件的Resource
        Resource[] configResources = getConfigResources();
        if (configResources != null) {
            // 加载BeanDefinition
            reader.loadBeanDefinitions(configResources);
        }
        // xml还没加载成Resource, 
        // 先获取xml配置文件的路径, 
        String[] configLocations = getConfigLocations();
        if (configLocations != null) {
            // 先把xml配置文件加载成Resource, 
            // 再去加载BeanDefinition
            reader.loadBeanDefinitions(configLocations);
        }
    }
}

public abstract class AbstractBeanDefinitionReader implements EnvironmentCapable, BeanDefinitionReader {

    public int loadBeanDefinitions(Resource... resources) throws BeanDefinitionStoreException {
        int counter = 0;
        for (Resource resource : resources) {
            // 调用XmlBeanDefinitionReader::loadBeanDefinitions()方法
            counter += loadBeanDefinitions(resource);
        }
        return counter;
    }
}
```
