# 创建单例bean

```java
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    protected <T> T doGetBean(String name, @Nullable Class<T> requiredType, @Nullable Object[] args, boolean typeCheckOnly)
            throws BeansException {
        String beanName = transformedBeanName(name);
        Object bean;

        // ...
        // 单例模式实例化bean
        if (mbd.isSingleton()) {
            sharedInstance = getSingleton(beanName, () -> {
                try {
                    // 创建bean
                    return createBean(beanName, mbd, args);
                } catch (BeansException ex) {
                    destroySingleton(beanName);
                    throw ex;
                }
            });
            bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
        }
        // ...

        return (T) bean;
    }
}

public class DefaultSingletonBeanRegistry extends SimpleAliasRegistry implements SingletonBeanRegistry {

    /**
     * 单例模式实例化bean
     */
    public Object getSingleton(String beanName, ObjectFactory<?> singletonFactory) {
        synchronized (this.singletonObjects) {
            // 从一级缓存中获取
            Object singletonObject = this.singletonObjects.get(beanName);
            if (singletonObject == null) {
                // 判断这个bean是否正在销毁
                if (this.singletonsCurrentlyInDestruction) {
                    throw new BeanCreationNotAllowedException(beanName,
                            "Singleton bean creation not allowed while singletons of this factory are in destruction " +
                                    "(Do not request a bean from a BeanFactory in a destroy method implementation!)");
                }
                // 添加到singletonsCurrentlyInCreation缓存中
                beforeSingletonCreation(beanName);
                // 是否为新创建的单例对象, 用于判断是否需要缓存
                boolean newSingleton = false;
                // suppressedExceptions用于记录bean创建过程中的异常
                boolean recordSuppressedExceptions = (this.suppressedExceptions == null);
                if (recordSuppressedExceptions) {
                    this.suppressedExceptions = new LinkedHashSet<>();
                }
                try {
                    // 使用单例工厂创建bean
                    // singletonFactory是doGetBean传进来的
                    /*
                        () -> {
                            try {
                                return createBean(beanName, mbd, args);
                            } catch (BeansException ex) {
                                destroySingleton(beanName);
                                throw ex;
                            }
                        }
                    */
                    singletonObject = singletonFactory.getObject();
                    // 需要缓存
                    newSingleton = true;
                } catch (IllegalStateException ex) {
                    // 再试着从一级缓存中获取
                    singletonObject = this.singletonObjects.get(beanName);
                    if (singletonObject == null) {
                        throw ex;
                    }
                } catch (BeanCreationException ex) {
                    if (recordSuppressedExceptions) {
                        for (Exception suppressedException : this.suppressedExceptions) {
                            ex.addRelatedCause(suppressedException);
                        }
                    }
                    throw ex;
                } finally {
                    if (recordSuppressedExceptions) {
                        this.suppressedExceptions = null;
                    }
                    // 从singletonsCurrentlyInCreation缓存中移除
                    afterSingletonCreation(beanName);
                }
                if (newSingleton) {
                    // 添加到一级缓存中
                    addSingleton(beanName, singletonObject);
                }
            }
            return singletonObject;
        }
    }
}
```

