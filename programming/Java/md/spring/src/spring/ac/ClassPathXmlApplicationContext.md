# ClassPathXmlApplicationContext

```java
public class ClassPathXmlApplicationContext extends AbstractXmlApplicationContext {

    public ClassPathXmlApplicationContext(String configLocation) throws BeansException {
        this(new String[]{configLocation}, true, null);
    }

    public ClassPathXmlApplicationContext(
            String[] configLocations, boolean refresh, @Nullable ApplicationContext parent)
            throws BeansException {
        super(parent);
        setConfigLocations(configLocations);
        if (refresh) {
            refresh();
        }
    }

    /**
     * 把xml配置文件设置configLocations字段中
     */
    public void setConfigLocations(@Nullable String... locations) {
        if (locations != null) {
            this.configLocations = new String[locations.length];
            for (int i = 0; i < locations.length; i++) {
                // resolvePath()方法主要用于解析给定的路径数组，
                // 如果数组中包含特殊符号，如${var}，
                // 那么在resoIvePath()中会搜寻匹配的系统变量并替换
                this.configLocations[i] = resolvePath(locations[i]).trim();
            }
        }
        else {
            this.configLocations = null;
        }
    }
}

public abstract class AbstractApplicationContext extends DefaultResourceLoader
        implements ConfigurableApplicationContext {
    
    public void refresh() throws BeansException, IllegalStateException {
        synchronized (this.startupShutdownMonitor) {
            // 准备工作
            prepareRefresh();
            // 初始化BeanFactory，并读取xml文件
            ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
            // 扩展BeanFactory
            prepareBeanFactory(beanFactory);
            try {
                // 空方法，留给子类覆盖，做自定义业务处理
                postProcessBeanFactory(beanFactory);
                // 激活各种BeanFactory后置处理器
                invokeBeanFactoryPostProcessors(beanFactory);
                // 注册bean的后置处理器，bean创建时的拦截器
                registerBeanPostProcessors(beanFactory);
                // 对消息做国际化处理
                initMessageSource();
                // 初始化事件监听多路广播器
                initApplicationEventMulticaster();
                // 空方法，留给子类覆盖，初始化特定的bean
                onRefresh();
                // 注册监听器
                registerListeners();
                // 实例化所有剩余的非懒加载单例bean
                finishBeanFactoryInitialization(beanFactory);
                // refresh完成，发出通知
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
