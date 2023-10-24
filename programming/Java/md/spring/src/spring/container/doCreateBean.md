# 常规创建bean

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) throws BeanCreationException {

        RootBeanDefinition mbdToUse = mbd;
        // ...
        // 处理Spring的后置处理器
        // ...
        try {
            // 实际创建bean
            Object beanInstance = doCreateBean(beanName, mbdToUse, args);
            return beanInstance;
        } catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
            throw ex;
        } catch (Throwable ex) {
            throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName, "Unexpected exception during bean creation", ex);
        }
    }
}
```
