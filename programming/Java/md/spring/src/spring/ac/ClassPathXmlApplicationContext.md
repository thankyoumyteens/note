# ClassPathXmlApplicationContext

ClassPathXmlApplicationContext 是 Spring 框架中用于从类路径下加载 XML 配置文件并初始化 Spring 容器的一种方式。它是 ApplicationContext 接口的实现类之一，通过读取类路径下的 XML 配置文件，可以实例化和管理 Spring 容器中的各种 Bean。

```java
public class ClassPathXmlApplicationContext extends AbstractXmlApplicationContext {

    public ClassPathXmlApplicationContext(String configLocation) throws BeansException {
        this(new String[]{configLocation}, true, null);
    }

    public ClassPathXmlApplicationContext(
            String[] configLocations, boolean refresh, @Nullable ApplicationContext parent)
            throws BeansException {
        super(parent);
        // 记录xml配置文件
        setConfigLocations(configLocations);
        if (refresh) {
            refresh();
        }
    }
}

public abstract class AbstractRefreshableConfigApplicationContext
        extends AbstractRefreshableApplicationContext
        implements BeanNameAware, InitializingBean {
    /**
     * 把xml配置文件保存到configLocations字段中
     */
    public void setConfigLocations(@Nullable String... locations) {
        if (locations != null) {
            this.configLocations = new String[locations.length];
            for (int i = 0; i < locations.length; i++) {
                // resolvePath()方法主要用于解析给定的路径数组,
                // 如果数组中包含特殊符号, 如${var},
                // 那么在resoIvePath()中会搜寻匹配的系统变量并替换
                this.configLocations[i] = resolvePath(locations[i]).trim();
            }
        }
        else {
            this.configLocations = null;
        }
    }
}
```

## refresh 方法

```java
public abstract class AbstractApplicationContext extends DefaultResourceLoader
        implements ConfigurableApplicationContext {

    public void refresh() throws BeansException, IllegalStateException {
        // startupShutdownMonitor是专门给refresh和destroy两个方法加锁用的:
        // private final Object startupShutdownMonitor = new Object();
        synchronized (this.startupShutdownMonitor) {
            // refresh的准备工作
            prepareRefresh();
            // 创建BeanFactory, 在这里会加载BeanDefinition
            ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
            // 扩展BeanFactory
            prepareBeanFactory(beanFactory);
            try {
                // 空方法, 留给子类覆盖, 做自定义业务处理
                postProcessBeanFactory(beanFactory);
                // 激活各种BeanFactory后置处理器
                invokeBeanFactoryPostProcessors(beanFactory);
                // 注册bean的后置处理器, bean创建时的拦截器
                registerBeanPostProcessors(beanFactory);
                // 对消息做国际化处理
                initMessageSource();
                // 初始化事件监听多路广播器
                initApplicationEventMulticaster();
                // 空方法, 留给子类覆盖, 初始化特定的bean
                onRefresh();
                // 注册监听器
                registerListeners();
                // 实例化所有剩余的非懒加载单例bean
                finishBeanFactoryInitialization(beanFactory);
                // refresh完成, 发出通知
                finishRefresh();
            } catch (BeansException ex) {
                destroyBeans();
                cancelRefresh(ex);
                throw ex;
            } finally {
                resetCommonCaches();
            }
        }
    }
}
```
