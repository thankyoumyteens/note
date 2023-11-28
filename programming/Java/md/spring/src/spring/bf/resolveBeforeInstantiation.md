# Spring的后置处理器

Spring的后置处理器InstantiationAwareBeanPostProcessor可以让用户在bean初始化前和初始化后的瞬间, 添加一些自定义处理。

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) throws BeanCreationException {

        RootBeanDefinition mbdToUse = mbd;
        // ...
        try {
            // 处理Spring的后置处理器
            Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
            if (bean != null) {
                return bean;
            }
        } catch (Throwable ex) {
            throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName, "BeanPostProcessor before instantiation of bean failed", ex);
        }
        // ...
    }

    /**
     * 处理Spring的后置处理器
     */
    protected Object resolveBeforeInstantiation(String beanName, RootBeanDefinition mbd) {
        Object bean = null;
        if (!Boolean.FALSE.equals(mbd.beforeInstantiationResolved)) {
            // 判断这个bean是否配置了后置处理器: InstantiationAwareBeanPostProcessor
            if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
                // 获取bean的Class
                Class<?> targetType = determineTargetType(beanName, mbd);
                if (targetType != null) {
                    // 执行后置处理器在初始化前的自定义处理
                    bean = applyBeanPostProcessorsBeforeInstantiation(targetType, beanName);
                    if (bean != null) {
                        // 如果bean被替换了, 则表示这个bean已经初始化完成了
                        // 需要执行后置处理器在初始化后的自定义处理
                        bean = applyBeanPostProcessorsAfterInitialization(bean, beanName);
                    }
                }
            }
            mbd.beforeInstantiationResolved = (bean != null);
        }
        return bean;
    }

    /**
     * 初始化前添加自定义处理
     */
    protected Object applyBeanPostProcessorsBeforeInstantiation(Class<?> beanClass, String beanName) {
        // 遍历配置的后处理器
        for (BeanPostProcessor bp : getBeanPostProcessors()) {
            if (bp instanceof InstantiationAwareBeanPostProcessor) {
                InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
                // 可以重写postProcessBeforeInstantiation()方法返回一个代理对象, 
                // 替换掉原本的bean对象
                Object result = ibp.postProcessBeforeInstantiation(beanClass, beanName);
                if (result != null) {
                    return result;
                }
            }
        }
        return null;
    }

    /**
     * 初始化后添加自定义处理
     */
    public Object applyBeanPostProcessorsAfterInitialization(Object existingBean, String beanName)
            throws BeansException {

        Object result = existingBean;
        // 遍历配置的后处理器
        for (BeanPostProcessor processor : getBeanPostProcessors()) {
            // 可以重写postProcessAfterInitialization()方法, 做自己的处理
            Object current = processor.postProcessAfterInitialization(result, beanName);
            if (current == null) {
                return result;
            }
            result = current;
        }
        return result;
    }
}
```
