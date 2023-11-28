# SpEL 语言支持

Spring 表达式语言(Spring Expression Language, SpEL), 能在运行时构建复杂表达式、存取对象图属性、对象方法调用等。SpEL 是单独模块, 只依赖于 core 模块, 不依赖于其他模块, 可以单独使用。

SpEL 使用`#{}`作为定界符, 所有在大括号中的字符都将被认为是 SpEL。

## 注册 SpEL 的解析器

```java
public abstract class AbstractApplicationContext extends DefaultResourceLoader
        implements ConfigurableApplicationContext {

    protected void prepareBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        // ...
        beanFactory.setBeanExpressionResolver(new StandardBeanExpressionResolver(beanFactory.getBeanClassLoader()));
        // ...
    }
}
```

## SpEL 解析器的调用时机

在填充 bean 属性的时候, 会调用 SpEL 解析器

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {

    /**
     * 填充bean属性
     */
    protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
        // ...
        // 获取自动装配类型
        int resolvedAutowireMode = mbd.getResolvedAutowireMode();
        if (resolvedAutowireMode == AUTOWIRE_BY_NAME || resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
            MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
            // ...
            // byType, 找出和字段类型相同的bean, 存入newPvs中
            if (resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
                autowireByType(beanName, mbd, bw, newPvs);
            }
            pvs = newPvs;
        }
        // ...
    }

    /**
     * byType
     */
    protected void autowireByType(
            String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {

        // ...
        Object autowiredArgument = resolveDependency(desc, beanName, autowiredBeanNames, converter);
        // ...
    }
}

public class DefaultListableBeanFactory extends AbstractAutowireCapableBeanFactory
        implements ConfigurableListableBeanFactory, BeanDefinitionRegistry, Serializable {

    /**
     * 解析指定依赖项
     */
    public Object resolveDependency(DependencyDescriptor descriptor, @Nullable String requestingBeanName,
                                    @Nullable Set<String> autowiredBeanNames, @Nullable TypeConverter typeConverter) throws BeansException {

        // ...
        if (result == null) {
            // 解析指定依赖项
            result = doResolveDependency(descriptor, requestingBeanName, autowiredBeanNames, typeConverter);
        }
        // ...
    }

    @Nullable
    public Object doResolveDependency(DependencyDescriptor descriptor, @Nullable String beanName,
                                      @Nullable Set<String> autowiredBeanNames, @Nullable TypeConverter typeConverter) throws BeansException {

        InjectionPoint previousInjectionPoint = ConstructorResolver.setCurrentInjectionPoint(descriptor);
        try {
            Object shortcut = descriptor.resolveShortcut(this);
            if (shortcut != null) {
                return shortcut;
            }

            Class<?> type = descriptor.getDependencyType();
            // 处理@Value注解
            Object value = getAutowireCandidateResolver().getSuggestedValue(descriptor);
            if (value != null) {
                if (value instanceof String) {
                    String strVal = resolveEmbeddedValue((String) value);
                    BeanDefinition bd = (beanName != null && containsBean(beanName) ? getMergedBeanDefinition(beanName) : null);
                    value = evaluateBeanDefinitionString(strVal, bd);
                }
                TypeConverter converter = (typeConverter != null ? typeConverter : getTypeConverter());
                return (descriptor.getField() != null ?
                        converter.convertIfNecessary(value, type, descriptor.getField()) :
                        converter.convertIfNecessary(value, type, descriptor.getMethodParameter()));
            }
            // ...
            return result;
        } finally {
            ConstructorResolver.setCurrentInjectionPoint(previousInjectionPoint);
        }
    }
}

public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    /**
     * 使用SpEL解析器
     */
    protected Object evaluateBeanDefinitionString(@Nullable String value, @Nullable BeanDefinition beanDefinition) {
        if (this.beanExpressionResolver == null) {
            return value;
        }

        Scope scope = null;
        if (beanDefinition != null) {
            String scopeName = beanDefinition.getScope();
            if (scopeName != null) {
                scope = getRegisteredScope(scopeName);
            }
        }
        return this.beanExpressionResolver.evaluate(value, new BeanExpressionContext(this, scope));
    }
}
```
