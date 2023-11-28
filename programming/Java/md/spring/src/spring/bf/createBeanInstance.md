# 创建bean对象

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {

    /**
     * 创建bean对象
     */
    protected BeanWrapper createBeanInstance(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) {
        // 获取bean的Class
        Class<?> beanClass = resolveBeanClass(mbd, beanName);
        // 校验Class的可访问性
        if (beanClass != null && !Modifier.isPublic(beanClass.getModifiers()) && !mbd.isNonPublicAccessAllowed()) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                    "Bean class isn't public, and non-public access not allowed: " + beanClass.getName());
        }
        // 使用Supplier创建bean
        Supplier<?> instanceSupplier = mbd.getInstanceSupplier();
        if (instanceSupplier != null) {
            return obtainFromSupplier(instanceSupplier, beanName);
        }
        // 使用工厂创建bean
        if (mbd.getFactoryMethodName() != null) {
            return instantiateUsingFactoryMethod(beanName, mbd, args);
        }

        // 在prototype模式下, 如果已经创建过一次这个bean了, 
        // 那么就不需要再次判断要调用哪个构造方法或者工厂方法了
        boolean resolved = false;
        // 是否自动装配
        boolean autowireNecessary = false;
        if (args == null) {
            // 判断是否已经确定过了要使用的构造方法或者工厂方法
            synchronized (mbd.constructorArgumentLock) {
                // 要使用的构造方法或者工厂方法会放在resolvedConstructorOrFactoryMethod中
                // 如果不为空, 表示已经创建过一次这个bean了
                if (mbd.resolvedConstructorOrFactoryMethod != null) {
                    resolved = true;
                    // 是否设置了autowire="constructor"自动装配
                    autowireNecessary = mbd.constructorArgumentsResolved;
                }
            }
        }
        // 在prototype模式下, 再次创建bean
        if (resolved) {
            if (autowireNecessary) {
                // 处理autowire="constructor"自动装配, 并创建bean
                return autowireConstructor(beanName, mbd, null, null);
            } else {
                // 使用默认无参构造方法创建bean
                return instantiateBean(beanName, mbd);
            }
        }
        // 通过后置处理器SmartInstantiationAwareBeanPostProcessor获取指定构造方法
        Constructor<?>[] ctors = determineConstructorsFromBeanPostProcessors(beanClass, beanName);
        // 判断: 
        // 1. 有没有指定构造方法
        // 2. 有没有autowire="constructor"自动装配
        // 3. 有没有构造方法参数
        if (ctors != null || mbd.getResolvedAutowireMode() == AUTOWIRE_CONSTRUCTOR ||
                mbd.hasConstructorArgumentValues() || !ObjectUtils.isEmpty(args)) {
            // 使用特定的构造方法创建bean
            return autowireConstructor(beanName, mbd, ctors, args);
        }

        // 使用默认无参构造方法创建bean
        return instantiateBean(beanName, mbd);
    }

    /**
     * 使用Supplier创建bean
     */
    protected BeanWrapper obtainFromSupplier(Supplier<?> instanceSupplier, String beanName) {
        Object instance;
        // 把当前正在创建的beanNeame存储到ThreadLocal中, 用于标记
        String outerBean = this.currentlyCreatedBean.get();
        this.currentlyCreatedBean.set(beanName);
        try {
            // 使用Supplier获取bean
            // Supplier是JDK 8提供的函数式接口
            /*
                @FunctionalInterface
                public interface Supplier<T> {
                    T get();
                }
            */
            instance = instanceSupplier.get();
        } finally {
            if (outerBean != null) {
                this.currentlyCreatedBean.set(outerBean);
            } else {
                this.currentlyCreatedBean.remove();
            }
        }

        if (instance == null) {
            instance = new NullBean();
        }
        // 把bean放进包装类
        BeanWrapper bw = new BeanWrapperImpl(instance);
        // 初始化bean的包装类
        initBeanWrapper(bw);
        return bw;
    }
}
```
