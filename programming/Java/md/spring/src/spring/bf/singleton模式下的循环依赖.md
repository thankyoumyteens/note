# singleton模式下的循环依赖

Spring只能解决singleton模式下，通过setter注入的循环依赖。通过构造方法注入或prototype模式下的循环依赖，Spring无法解决。

spring解决循环依赖的过程中用到的Map缓存：

1. singletonObjects：一级缓存，这里面保存的是已经完成依赖注入的完整的bean
2. earlySingletonObjects：二级缓存，这个里面保存的是一个已经创建了对象，尚未依赖注入的bean
3. singletonFactories：三级缓存，这里面保存了一个ObjectFactory，它可以返回一个bean对象的引用
4. singletonsCurrentlyInCreation：创建中的beanName缓存，这个里面保存的是一个已经创建了对象，尚未依赖注入的bean的beanName

```java
public class TestA {
    @Resource
    private TestB testB;
}

public class TestB {
    @Resource
    private TestA testA;
}

TestA a = (TestA) bf.getBean("testA");
```

此时singleton模式下getBean的执行过程：

1. 首先从缓存中获取单例bean：testA
2. singletonObjects缓存中没有testA，并且singletonsCurrentlyInCreation缓存中也没有testA，直接返回null
3. 开始创建testA，首先把tastA添加到singletonsCurrentlyInCreation缓存中，表示testA正在创建中
4. 创建testA，并填充tastA的属性(给字段赋值，比如依赖注入)
5. spring发现testA中依赖了testB，会调用getBean()方法获取testB
6. 由于testB没有创建，所以也会开始执行创建过程
7. 首先从缓存中获取单例bean：testB
8. singletonObjects缓存中没有testB，并且singletonsCurrentlyInCreation缓存中也没有testB，直接返回null
9. 开始创建testB，首先把tastB添加到singletonsCurrentlyInCreation缓存中，表示testB正在创建中
10. 创建testB，并填充taseB的属性
11. 这时，spring发现testB中依赖了testA，会调用getBean()方法获取testA
12. 又会从缓存中获取单例bean：testA
13. singletonObjects缓存中没有testA，但是这时singletonsCurrentlyInCreation缓存中存在testA，spring会把testA对象的引用返回
14. testB中调用的getBean()方法返回testA对象的引用，把它赋值给testB中的testA属性
15. testB对象创建完成，从singletonsCurrentlyInCreation缓存中移除testB，并把它加到singletonObjects缓存中
16. testA对象创建完成，从singletonsCurrentlyInCreation缓存中移除testA，并把它加到singletonObjects缓存中

```java
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    protected <T> T doGetBean(String name, @Nullable Class<T> requiredType, @Nullable Object[] args, boolean typeCheckOnly)
            throws BeansException {
        String beanName = transformedBeanName(name);
        Object bean;

        // 先从单例缓存中获取
        Object sharedInstance = getSingleton(beanName);
        if (sharedInstance != null && args == null) {
            bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
        } else {
            // ...
            // 缓存中没有
            // 单例模式实例化bean
            if (mbd.isSingleton()) {
                sharedInstance = getSingleton(beanName, () -> {
                    try {
                        // 创建bean
                        return createBean(beanName, mbd, args);
                    } catch (BeansException ex) {
                        // 创建失败则清理这个bean留下的数据，比如已经添加的缓存
                        destroySingleton(beanName);
                        throw ex;
                    }
                });
                bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
            }
            // ...
        }

        return (T) bean;
    }
}

public class DefaultSingletonBeanRegistry extends SimpleAliasRegistry implements SingletonBeanRegistry {

    /**
     * 从缓存中获取
     */
    public Object getSingleton(String beanName) {
        return getSingleton(beanName, true);
    }

    /**
     * 从缓存中获取
     */
    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
        // singletonObjects就是单例缓存
        Object singletonObject = this.singletonObjects.get(beanName);
        // 缓存里没有，根据beanName判断bean是否已经创建了对象，但还没有依赖注入
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            synchronized (this.singletonObjects) {
                // 从earlySingletonObjects缓存中获取一个创建中的bean
                singletonObject = this.earlySingletonObjects.get(beanName);
                // allowEarlyReference为true表示需要解决循环依赖，允许返回一个没有创建完成的bean
                if (singletonObject == null && allowEarlyReference) {
                    // singletonFactory：单例工厂，返回一个创建中的bean的引用
                    ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                    if (singletonFactory != null) {
                        // 获取创建中的bean的引用
                        // getObject()并不会创建bean，只是找到对应的bean并返回
                        singletonObject = singletonFactory.getObject();
                        // 缓存这个引用
                        this.earlySingletonObjects.put(beanName, singletonObject);
                        // 这个工厂用完了不会再用，删除
                        this.singletonFactories.remove(beanName);
                    }
                }
            }
        }
        return singletonObject;
    }

    /**
     * 单例模式实例化bean
     * sharedInstance = getSingleton(beanName, () -> {
     *     try {
     *         return createBean(beanName, mbd, args);
     *     } catch (BeansException ex) {
     *         destroySingleton(beanName);
     *         throw ex;
     *     }
     * });
     */
    public Object getSingleton(String beanName, ObjectFactory<?> singletonFactory) {
        synchronized (this.singletonObjects) {
            Object singletonObject = this.singletonObjects.get(beanName);
            if (singletonObject == null) {
                // ...
                // 把正在创建的bean添加到singletonsCurrentlyInCreation缓存中
                beforeSingletonCreation(beanName);
                // ...
                try {
                    // 创建bean
                    // 在这里会给singletonFactories赋值
                    singletonObject = singletonFactory.getObject();
                    // ...
                } finally {
                    // bean对象创建完成，从singletonsCurrentlyInCreation缓存中移除
                    afterSingletonCreation(beanName);
                }
                if (newSingleton) {
                    // 添加到singletonObjects缓存中
                    addSingleton(beanName, singletonObject);
                }
            }
            return singletonObject;
        }
    }
}

public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    /**
     * singletonObject = singletonFactory.getObject();会调用到这里
     * 创建bean
     */
    protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) throws BeanCreationException {

        RootBeanDefinition mbdToUse = mbd;

        // ...
        try {
            // 常规创建bean
            Object beanInstance = doCreateBean(beanName, mbdToUse, args);
            return beanInstance;
        } catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
            // ...
        }
    }

    protected Object doCreateBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) throws BeanCreationException {

        // ...
        // 用于解决循环依赖
        boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences && isSingletonCurrentlyInCreation(beanName));
        if (earlySingletonExposure) {
            // 把单例工厂添加到三级缓存中
            // getEarlyBeanReference()返回当前正在创建的bean的引用
            // 第三个参数bean就是当前正在创建的bean对象
            addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
        }
        // ...
        // 填充bean的属性，注入属性值，如果依赖其它的bean，会递归去初始化其它的bean
        populateBean(beanName, mbd, instanceWrapper);
        // ...
    }

    /**
     * 返回bean的引用
     */
    protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
        Object exposedObject = bean;
        if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
            // 执行后置处理器
            for (BeanPostProcessor bp : getBeanPostProcessors()) {
                if (bp instanceof SmartInstantiationAwareBeanPostProcessor) {
                    // 后置处理器可能返回一个代理对象取代原有的bean
                    SmartInstantiationAwareBeanPostProcessor ibp = (SmartInstantiationAwareBeanPostProcessor) bp;
                    exposedObject = ibp.getEarlyBeanReference(exposedObject, beanName);
                }
            }
        }
        // 如果bean没有被替换，则返回传入的bean
        // 如果bean被替换了，则返回替换后的bean
        return exposedObject;
    }
}
```
