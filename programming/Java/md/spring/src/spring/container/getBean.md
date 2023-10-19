# getBean

XmlBeanFactory的getBean()方法，调用的是祖先类AbstractBeanFactory中的方法。

```java
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    public Object getBean(String name) throws BeansException {
        return doGetBean(name, null, null, false);
    }

    protected <T> T doGetBean(String name, @Nullable Class<T> requiredType, @Nullable Object[] args, boolean typeCheckOnly)
            throws BeansException {
        // 获取beanName，name有可能传入别名
        String beanName = transformedBeanName(name);
        // bean的实例
        Object bean;

        // 从缓存中获取
        Object sharedInstance = getSingleton(beanName);
        if (sharedInstance != null && args == null) {
            // 如果 sharedInstance 是普通的 Bean 实例，则下面的方法会直接返回
            // 如果 sharedInstance 是FactoryBean类型，则需要调用它的getObject()方法获取bean
            bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
        } else {
            // 用于判断prototype模式下有没有循环依赖
            if (isPrototypeCurrentlyInCreation(beanName)) {
                // prototype模式不允许循环依赖，抛异常
                throw new BeanCurrentlyInCreationException(beanName);
            }
            // 缓存中没有，看看父级中有没有
            BeanFactory parentBeanFactory = getParentBeanFactory();
            // 到parentBeanFactory中查找有没有这个bean的BeanDefinition
            if (parentBeanFactory != null && !containsBeanDefinition(beanName)) {
                // 获取 name 对应的 beanName，如果 name 是以 & 开头，则返回 "&" + beanName
                String nameToLookup = originalBeanName(name);
                if (parentBeanFactory instanceof AbstractBeanFactory) {
                    return ((AbstractBeanFactory) parentBeanFactory).doGetBean(
                            nameToLookup, requiredType, args, typeCheckOnly);
                }else if (args != null) {
                    // 根据 args 参数是否为空，调用不同的父容器方法获取 bean 实例
                    return (T) parentBeanFactory.getBean(nameToLookup, args);
                } else {
                    // 根据 args 参数是否为空，调用不同的父容器方法获取 bean 实例
                    return parentBeanFactory.getBean(nameToLookup, requiredType);
                }
            }

            // typeCheckOnly用于判断调用 getBean 方法时，是否只是做类型检查
            if (!typeCheckOnly) {
                // 标记bean已实例化
                markBeanAsCreated(beanName);
            }

            try {
                // 从DefaultListableBeanFactory的BeanDefinition缓存中获取beanName对应的 GenericBeanDefinition，并转换为 RootBeanDefinition
                RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
                // 检查当前创建的 bean 定义是否为抽象 bean 定义
                checkMergedBeanDefinition(mbd, beanName, args);

                // 寻找依赖
                String[] dependsOn = mbd.getDependsOn();
                if (dependsOn != null) {
                    for (String dep : dependsOn) {
                        // 监测是否存在 depends-on 循环依赖，若存在则会抛出异常
                        if (isDependent(beanName, dep)) {
                            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                                    "Circular depends-on relationship between '" + beanName + "' and '" + dep + "'");
                        }
                        // 注册依赖记录
                        registerDependentBean(dep, beanName);
                        try {
                            // 先加载依赖的 bean
                            getBean(dep);
                        } catch (NoSuchBeanDefinitionException ex) {
                            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                                    "'" + beanName + "' depends on missing bean '" + dep + "'", ex);
                        }
                    }
                }

                // 实例化bean
                if (mbd.isSingleton()) {
                    // 单例模式
                    sharedInstance = getSingleton(beanName, () -> {
                        try {
                            // 创建 bean
                            return createBean(beanName, mbd, args);
                        } catch (BeansException ex) {
                            // 创建失败则销毁
                            destroySingleton(beanName);
                            throw ex;
                        }
                    });
                    // 如果 sharedInstance 是普通的 Bean 实例，则下面的方法会直接返回
                    // 如果 sharedInstance 是FactoryBean类型，则需要调用它的getObject()方法获取bean
                    bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
                } else if (mbd.isPrototype()) {
                    // prototype模式
                    Object prototypeInstance = null;
                    try {
                        // 把beanName记录prototypesCurrentlyInCreation，表示正在创建，还没创建完
                        beforePrototypeCreation(beanName);
                        // 创建bean
                        prototypeInstance = createBean(beanName, mbd, args);
                    } finally {
                        // 创建完了，把beanName从prototypesCurrentlyInCreation中删掉
                        afterPrototypeCreation(beanName);
                    }
                    // 如果 sharedInstance 是普通的 Bean 实例，则下面的方法会直接返回
                    // 如果 sharedInstance 是FactoryBean类型，则需要调用它的getObject()方法获取bean
                    bean = getObjectForBeanInstance(prototypeInstance, name, beanName, mbd);
                } else {
                    // 指定的scope上实例化bean
                    String scopeName = mbd.getScope();
                    if (!StringUtils.hasLength(scopeName)) {
                        throw new IllegalStateException("No scope name defined for bean ´" + beanName + "'");
                    }
                    Scope scope = this.scopes.get(scopeName);
                    if (scope == null) {
                        throw new IllegalStateException("No Scope registered for scope name '" + scopeName + "'");
                    }
                    try {
                        Object scopedInstance = scope.get(beanName, () -> {
                            beforePrototypeCreation(beanName);
                            try {
                                return createBean(beanName, mbd, args);
                            } finally {
                                afterPrototypeCreation(beanName);
                            }
                        });
                        bean = getObjectForBeanInstance(scopedInstance, name, beanName, mbd);
                    } catch (IllegalStateException ex) {
                        throw new BeanCreationException(beanName,
                                "Scope '" + scopeName + "' is not active for the current thread; consider " +
                                "defining a scoped proxy for this bean if you intend to refer to it from a singleton",
                                ex);
                    }
                }
            } catch (BeansException ex) {
                cleanupAfterBeanCreationFailure(beanName);
                throw ex;
            }
        }

        // 如果需要类型转换，这里会进行操作
        if (requiredType != null && !requiredType.isInstance(bean)) {
            try {
                T convertedBean = getTypeConverter().convertIfNecessary(bean, requiredType);
                if (convertedBean == null) {
                    throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
                }
                return convertedBean;
            } catch (TypeMismatchException ex) {
                throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
            }
        }
        return (T) bean;
    }
}
```
