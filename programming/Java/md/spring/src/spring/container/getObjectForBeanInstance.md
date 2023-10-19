# getObjectForBeanInstance

getObjectForBeanInstance()方法会根据传入的sharedInstance做不同的处理。如果 sharedInstance 是普通的 Bean 实例，则会直接返回，如果 sharedInstance 是FactoryBean类型，则需要调用FactoryBean的getObject()方法获取bean，再返回。

## FactoryBean

FactoryBean通常是用来创建比较复杂的bean，一般的bean直接用xml配置即可，但如果一个bean的创建过程中涉及到很多其他的bean和复杂的逻辑，用xml配置比较困难，这时可以考虑用FactoryBean。

当配置文件中bean的的class属性配置的是FactoryBean的实现类时，Spring的getBean()方法返回的就不是这个FactoryBean对象本身，而是会调用FactoryBean::getObject()方法，最终会把FactoryBean::getObject()的返回值作为结果返回。

如果想要获取FactoryBean对象本身，则需要在调用getBean()方法时，在beanName前加`&`符号，如：getBean("&testBean")。

```java
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    protected <T> T doGetBean(String name, @Nullable Class<T> requiredType, @Nullable Object[] args, boolean typeCheckOnly)
            throws BeansException {
        String beanName = transformedBeanName(name);
        Object bean;
        Object sharedInstance = getSingleton(beanName);
        if (sharedInstance != null && args == null) {
            // 如果 sharedInstance 是普通的 Bean 实例，则下面的方法会直接返回
            // 如果 sharedInstance 是FactoryBean类型，则需要调用它的getObject()方法获取bean
            bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
        } else {
            // ...
        }
        // ...
        return (T) bean;
    }

    protected Object getObjectForBeanInstance(Object beanInstance, String name, String beanName, @Nullable RootBeanDefinition mbd) {

        // 判断用户是不是要获取FactoryBean(使用&+beanName的方式)
        if (BeanFactoryUtils.isFactoryDereference(name)) {
            if (beanInstance instanceof NullBean) {
                return beanInstance;
            }
            // 不是FactoryBean，抛异常
            if (!(beanInstance instanceof FactoryBean)) {
                throw new BeanIsNotAFactoryException(beanName, beanInstance.getClass());
            }
        }

        // 执行到这里，说明beanInstance不是bean，就是FactoryBean
        // 如果不是FactoryBean类型，就表示beanInstance是bean实例，直接返回
        // 如果name是&+beanName的形式，则表示用户想要获取FactoryBean，也可以直接返回
        if (!(beanInstance instanceof FactoryBean) || BeanFactoryUtils.isFactoryDereference(name)) {
            return beanInstance;
        }
        // 执行到这里，说明用户想要一个bean，而且beanInstance是一个FactoryBean
        Object object = null;
        // 不传mbd，表示想先从缓存中获取
        if (mbd == null) {
            // 先尝试从缓存中获取
            object = getCachedObjectForFactoryBean(beanName);
        }
        // 缓存中没有
        if (object == null) {
            // 从FactoryBean中获取bean实例
            FactoryBean<?> factory = (FactoryBean<?>) beanInstance;
            // 如果从FactoryBean获取的对象是单例的，则将其缓存
            // 判断DefaultListableBeanFactory的BeanDefinition缓存中有没有beanName对应的 BeanDefinition
            if (mbd == null && containsBeanDefinition(beanName)) {
                // 如果的缓存中没有BeanDefinition，需要获取一个
                mbd = getMergedLocalBeanDefinition(beanName);
            }
            // isSynthetic()方法在创建AOP时候为true
            boolean synthetic = (mbd != null && mbd.isSynthetic());
            // 从FactoryBean中获取bean
            object = getObjectFromFactoryBean(factory, beanName, !synthetic);
        }
        return object;
    }

    // BeanFactoryUtils中的方法
    public static boolean isFactoryDereference(@Nullable String name) {
        // String FACTORY_BEAN_PREFIX = "&";
        return (name != null && name.startsWith(BeanFactory.FACTORY_BEAN_PREFIX));
    }

    protected Object getCachedObjectForFactoryBean(String beanName) {
        // Map<String, Object>类型的缓存
        return this.factoryBeanObjectCache.get(beanName);
    }

    // DefaultListableBeanFactory中的方法
    public boolean containsBeanDefinition(String beanName) {
        return this.beanDefinitionMap.containsKey(beanName);
    }
}
```
