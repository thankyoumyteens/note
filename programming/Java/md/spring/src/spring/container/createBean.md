# 创建bean

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    /**
     * singletonObject = singletonFactory.getObject();会调用到这里
     * 创建bean
     */
    protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) throws BeanCreationException {

        RootBeanDefinition mbdToUse = mbd;

        // 获取bean的Class对象
        Class<?> resolvedClass = resolveBeanClass(mbd, beanName);
        if (resolvedClass != null && !mbd.hasBeanClass() && mbd.getBeanClassName() != null) {
            mbdToUse = new RootBeanDefinition(mbd);
            mbdToUse.setBeanClass(resolvedClass);
        }

        try {
            // 验证lookup-method、replaced-method配置的替换方法
            mbdToUse.prepareMethodOverrides();
        } catch (BeanDefinitionValidationException ex) {
            throw new BeanDefinitionStoreException(mbdToUse.getResourceDescription(), beanName, "Validation of method overrides failed", ex);
        }

        try {
            // 处理Spring的后置处理器
            Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
            if (bean != null) {
                return bean;
            }
        } catch (Throwable ex) {
            throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName, "BeanPostProcessor before instantiation of bean failed", ex);
        }

        try {
            // 常规创建bean
            Object beanInstance = doCreateBean(beanName, mbdToUse, args);
            return beanInstance;
        } catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
            throw ex;
        } catch (Throwable ex) {
            throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName, "Unexpected exception during bean creation", ex);
        }
    }
}

public abstract class AbstractBeanDefinition extends BeanMetadataAttributeAccessor
        implements BeanDefinition, Cloneable {

    /**
     * 验证lookup-method/replaced-method配置的替换方法
     */
    public void prepareMethodOverrides() throws BeanDefinitionValidationException {
        // 判断methodOverrides缓存中是否有值
        if (hasMethodOverrides()) {
            // 遍历methodOverrides中的方法，每个方法都放到prepareMethodOverride()方法中处理一下
            getMethodOverrides().getOverrides().forEach(this::prepareMethodOverride);
        }
    }

    protected void prepareMethodOverride(MethodOverride mo) throws BeanDefinitionValidationException {
        // 判断bean中是否有要被替换的方法
        // mo.getMethodName()返回lookup-method/replaced-method中配置的要被替换的方法
        int count = ClassUtils.getMethodCountForName(getBeanClass(), mo.getMethodName());
        if (count == 0) {
            // 方法不存在
            throw new BeanDefinitionValidationException(
                    "Invalid method override: no method with name '" + mo.getMethodName() +
                            "' on class [" + getBeanClassName() + "]");
        } else if (count == 1) {
            // 这个方法没有重载版本，
            // 设置标记，这样在后续调用的时候便可以直接使用找到的方法，
            // 而不需要进行方法的参数匹配验证
            mo.setOverloaded(false);
        }
    }
}
```
