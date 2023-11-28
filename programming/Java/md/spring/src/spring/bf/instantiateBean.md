# 使用默认无参构造方法创建 bean

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {

    protected BeanWrapper instantiateBean(String beanName, RootBeanDefinition mbd) {
        try {
            Object beanInstance;
            if (System.getSecurityManager() != null) {
                // 先权限校验, 再创建对象
                beanInstance = AccessController.doPrivileged(
                        (PrivilegedAction<Object>) () -> getInstantiationStrategy().instantiate(mbd, beanName, this),
                        getAccessControlContext());
            } else {
                // 直接创建对象
                beanInstance = getInstantiationStrategy().instantiate(mbd, beanName, this);
            }
            // 把bean对象放入包装类
            BeanWrapper bw = new BeanWrapperImpl(beanInstance);
            initBeanWrapper(bw);
            return bw;
        } catch (Throwable ex) {
            throw new BeanCreationException(
                    mbd.getResourceDescription(), beanName, "Instantiation of bean failed", ex);
        }
    }
}

public class SimpleInstantiationStrategy implements InstantiationStrategy {

    public Object instantiate(RootBeanDefinition bd, @Nullable String beanName, BeanFactory owner) {
        // 判断是否需要替换方法
        if (!bd.hasMethodOverrides()) {
            // 不需要替换方法
            Constructor<?> constructorToUse;
            synchronized (bd.constructorArgumentLock) {
                // 先从缓存中找构造方法
                constructorToUse = (Constructor<?>) bd.resolvedConstructorOrFactoryMethod;
                if (constructorToUse == null) {
                    // 缓存里没有, 从Class中获取构造方法
                    final Class<?> clazz = bd.getBeanClass();
                    if (clazz.isInterface()) {
                        // 接口无法实例化, 抛异常
                        throw new BeanInstantiationException(clazz, "Specified class is an interface");
                    }
                    try {
                        if (System.getSecurityManager() != null) {
                            // 先校验权限, 再获取无参构造方法
                            constructorToUse = AccessController.doPrivileged(
                                    (PrivilegedExceptionAction<Constructor<?>>) clazz::getDeclaredConstructor);
                        } else {
                            // 获取无参构造方法
                            constructorToUse = clazz.getDeclaredConstructor();
                        }
                        // 缓存构造方法
                        bd.resolvedConstructorOrFactoryMethod = constructorToUse;
                    } catch (Throwable ex) {
                        throw new BeanInstantiationException(clazz, "No default constructor found", ex);
                    }
                }
            }
            // 创建对象
            return BeanUtils.instantiateClass(constructorToUse);
        } else {
            // 需要替换方法
            // 这个方法会被子类CglibSubclassingInstantiationStrategy重写
            // 通过cglib动态代理实现方法的替换
            return instantiateWithMethodInjection(bd, beanName, owner);
        }
    }
}

public abstract class BeanUtils {

    /**
     * 构造方法反射创建对象
     */
    public static <T> T instantiateClass(Constructor<T> ctor, Object... args) throws BeanInstantiationException {
        Assert.notNull(ctor, "Constructor must not be null");
        try {
            // 反射调用Constructor::newInstance()
            ReflectionUtils.makeAccessible(ctor);
            return (KotlinDetector.isKotlinType(ctor.getDeclaringClass()) ?
                    KotlinDelegate.instantiateClass(ctor, args) : ctor.newInstance(args));
        } catch (InstantiationException ex) {
            throw new BeanInstantiationException(ctor, "Is it an abstract class?", ex);
        } catch (IllegalAccessException ex) {
            throw new BeanInstantiationException(ctor, "Is the constructor accessible?", ex);
        } catch (IllegalArgumentException ex) {
            throw new BeanInstantiationException(ctor, "Illegal arguments for constructor", ex);
        } catch (InvocationTargetException ex) {
            throw new BeanInstantiationException(ctor, "Constructor threw exception", ex.getTargetException());
        }
    }
}
```
