# 使用工厂创建bean

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    /**
     * 使用工厂创建bean
     */
    protected BeanWrapper instantiateUsingFactoryMethod(String beanName, RootBeanDefinition mbd, @Nullable Object[] explicitArgs) {

        return new ConstructorResolver(this).instantiateUsingFactoryMethod(beanName, mbd, explicitArgs);
    }
}

class ConstructorResolver {

        public BeanWrapper instantiateUsingFactoryMethod(
            String beanName, RootBeanDefinition mbd, @Nullable Object[] explicitArgs) {

        // 初始化bean的包装类
        BeanWrapperImpl bw = new BeanWrapperImpl();
        this.beanFactory.initBeanWrapper(bw);

        Object factoryBean;
        Class<?> factoryClass;
        // 是否是静态方法
        boolean isStatic;
        // 获取工厂bean名称
        String factoryBeanName = mbd.getFactoryBeanName();
        if (factoryBeanName != null) {
            // 工厂bean和bean同名
            if (factoryBeanName.equals(beanName)) {
                throw new BeanDefinitionStoreException(mbd.getResourceDescription(), beanName,
                        "factory-bean reference points back to the same bean definition");
            }
            // 根据名称获取工厂
            factoryBean = this.beanFactory.getBean(factoryBeanName);
            // bean是单例，且工厂已经存在
            if (mbd.isSingleton() && this.beanFactory.containsSingleton(beanName)) {
                // 重复创建单例bean，报错
                throw new ImplicitlyAppearedSingletonException();
            }
            // 获取工厂的Class
            factoryClass = factoryBean.getClass();
            isStatic = false;
        } else {
            // 没有获取到工厂bean名称
            if (!mbd.hasBeanClass()) {
                // BeanDefinition里没有bean或工厂的Class
                throw new BeanDefinitionStoreException(mbd.getResourceDescription(), beanName,
                        "bean definition declares neither a bean class nor a factory-bean reference");
            }
            factoryBean = null;
            // 获取工厂的Class
            factoryClass = mbd.getBeanClass();
            isStatic = true;
        }

        Method factoryMethodToUse = null;
        ArgumentsHolder argsHolderToUse = null;
        Object[] argsToUse = null;
        // 如果指定了构造方法的参数，则构造bean的时候使用此构造方法
        if (explicitArgs != null) {
            argsToUse = explicitArgs;
        } else {
            Object[] argsToResolve = null;
            synchronized (mbd.constructorArgumentLock) {
                // 获取缓存起来的工厂方法/构造方法
                factoryMethodToUse = (Method) mbd.resolvedConstructorOrFactoryMethod;
                if (factoryMethodToUse != null && mbd.constructorArgumentsResolved) {
                    // 从缓存中获取参数
                    argsToUse = mbd.resolvedConstructorArguments;
                    if (argsToUse == null) {
                        argsToResolve = mbd.preparedConstructorArguments;
                    }
                }
            }
            // 如果缓存中存在，则解析存储在BeanDefinition中的参数
            if (argsToResolve != null) {
                argsToUse = resolvePreparedArguments(beanName, mbd, bw, factoryMethodToUse, argsToResolve);
            }
        }

        if (factoryMethodToUse == null || argsToUse == null) {
            // 获取工厂方法
            factoryClass = ClassUtils.getUserClass(factoryClass);
            Method[] rawCandidates = getCandidateMethods(factoryClass, mbd);
            List<Method> candidateList = new ArrayList<>();
            for (Method candidate : rawCandidates) {
                // 如果方法为静态方法，且为工厂方法则添加到candidateList中
                if (Modifier.isStatic(candidate.getModifiers()) == isStatic && mbd.isFactoryMethod(candidate)) {
                    candidateList.add(candidate);
                }
            }
            Method[] candidates = candidateList.toArray(new Method[0]);
            AutowireUtils.sortFactoryMethods(candidates);

            ConstructorArgumentValues resolvedValues = null;
            boolean autowiring = (mbd.getResolvedAutowireMode() == AutowireCapableBeanFactory.AUTOWIRE_CONSTRUCTOR);
            int minTypeDiffWeight = Integer.MAX_VALUE;
            Set<Method> ambiguousFactoryMethods = null;

            int minNrOfArgs;
            if (explicitArgs != null) {
                minNrOfArgs = explicitArgs.length;
            } else {
                // 如果getBean没有传递参数，则需要解析保存在BeanDefinition中的构造方法参数
                if (mbd.hasConstructorArgumentValues()) {
                    ConstructorArgumentValues cargs = mbd.getConstructorArgumentValues();
                    resolvedValues = new ConstructorArgumentValues();
                    minNrOfArgs = resolveConstructorArguments(beanName, mbd, bw, cargs, resolvedValues);
                } else {
                    minNrOfArgs = 0;
                }
            }

            LinkedList<UnsatisfiedDependencyException> causes = null;

            for (Method candidate : candidates) {
                // 获取工厂方法的参数列表
                Class<?>[] paramTypes = candidate.getParameterTypes();

                if (paramTypes.length >= minNrOfArgs) {
                    // 用来保存参数
                    ArgumentsHolder argsHolder;

                    if (explicitArgs != null) {
                        // 参数个数需要匹配
                        if (paramTypes.length != explicitArgs.length) {
                            continue;
                        }
                        argsHolder = new ArgumentsHolder(explicitArgs);
                    } else {
                        // 未提供参数
                        try {
                            String[] paramNames = null;
                            // ParameterNameDiscoverer用于寻找方法的参数名称列表
                            ParameterNameDiscoverer pnd = this.beanFactory.getParameterNameDiscoverer();
                            if (pnd != null) {
                                // 获取指定方法的参数名称列表
                                paramNames = pnd.getParameterNames(candidate);
                            }
                            argsHolder = createArgumentArray(
                                    beanName, mbd, resolvedValues, bw, paramTypes, paramNames, candidate, autowiring);
                        } catch (UnsatisfiedDependencyException ex) {
                            if (causes == null) {
                                causes = new LinkedList<>();
                            }
                            causes.add(ex);
                            continue;
                        }
                    }
                    // 判断解析方法的时候是否以宽松模式还是严格模式
                    // 严格模式：解析方法时，必须所有的参数都需要匹配，否则抛出异常
                    // 宽松模式：使用具有最接近的模式进行匹配
                    // typeDiffWeight：类型差异权重
                    int typeDiffWeight = (mbd.isLenientConstructorResolution() ?
                            argsHolder.getTypeDifferenceWeight(paramTypes) : argsHolder.getAssignabilityWeight(paramTypes));
                    // 选择最接近的一个方法
                    if (typeDiffWeight < minTypeDiffWeight) {
                        factoryMethodToUse = candidate;
                        argsHolderToUse = argsHolder;
                        argsToUse = argsHolder.arguments;
                        minTypeDiffWeight = typeDiffWeight;
                        ambiguousFactoryMethods = null;
                    }
                    // 如果具有相同参数数量的方法具有相同的typeDiffWeight
                    else if (factoryMethodToUse != null && typeDiffWeight == minTypeDiffWeight &&
                            !mbd.isLenientConstructorResolution() &&
                            paramTypes.length == factoryMethodToUse.getParameterCount() &&
                            !Arrays.equals(paramTypes, factoryMethodToUse.getParameterTypes())) {
                        if (ambiguousFactoryMethods == null) {
                            ambiguousFactoryMethods = new LinkedHashSet<>();
                            ambiguousFactoryMethods.add(factoryMethodToUse);
                        }
                        ambiguousFactoryMethods.add(candidate);
                    }
                }
            }
            // 没有可执行的工厂方法，抛出异常
            if (factoryMethodToUse == null) {
                if (causes != null) {
                    UnsatisfiedDependencyException ex = causes.removeLast();
                    for (Exception cause : causes) {
                        this.beanFactory.onSuppressedException(cause);
                    }
                    throw ex;
                }
                List<String> argTypes = new ArrayList<>(minNrOfArgs);
                if (explicitArgs != null) {
                    for (Object arg : explicitArgs) {
                        argTypes.add(arg != null ? arg.getClass().getSimpleName() : "null");
                    }
                } else if (resolvedValues != null) {
                    Set<ValueHolder> valueHolders = new LinkedHashSet<>(resolvedValues.getArgumentCount());
                    valueHolders.addAll(resolvedValues.getIndexedArgumentValues().values());
                    valueHolders.addAll(resolvedValues.getGenericArgumentValues());
                    for (ValueHolder value : valueHolders) {
                        String argType = (value.getType() != null ? ClassUtils.getShortName(value.getType()) :
                                (value.getValue() != null ? value.getValue().getClass().getSimpleName() : "null"));
                        argTypes.add(argType);
                    }
                }
                String argDesc = StringUtils.collectionToCommaDelimitedString(argTypes);
                throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "No matching factory method found: " +
                                (mbd.getFactoryBeanName() != null ?
                                        "factory bean '" + mbd.getFactoryBeanName() + "'; " : "") +
                                "factory method '" + mbd.getFactoryMethodName() + "(" + argDesc + ")'. " +
                                "Check that a method with the specified name " +
                                (minNrOfArgs > 0 ? "and arguments " : "") +
                                "exists and that it is " +
                                (isStatic ? "static" : "non-static") + ".");
            } else if (void.class == factoryMethodToUse.getReturnType()) {
                throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Invalid factory method '" + mbd.getFactoryMethodName() +
                                "': needs to have a non-void return type!");
            } else if (ambiguousFactoryMethods != null) {
                throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Ambiguous factory method matches found in bean '" + beanName + "' " +
                                "(hint: specify index/type/name arguments for simple parameters to avoid type ambiguities): " +
                                ambiguousFactoryMethods);
            }

            if (explicitArgs == null && argsHolderToUse != null) {
                argsHolderToUse.storeCache(mbd, factoryMethodToUse);
            }
        }

        try {
            Object beanInstance;
            // 验证权限
            if (System.getSecurityManager() != null) {
                final Object fb = factoryBean;
                final Method factoryMethod = factoryMethodToUse;
                final Object[] args = argsToUse;
                // 创建bean对象
                beanInstance = AccessController.doPrivileged((PrivilegedAction<Object>) () ->
                                beanFactory.getInstantiationStrategy().instantiate(mbd, beanName, beanFactory, fb, factoryMethod, args),
                        beanFactory.getAccessControlContext());
            } else {
                // 创建bean对象
                beanInstance = this.beanFactory.getInstantiationStrategy().instantiate(
                        mbd, beanName, this.beanFactory, factoryBean, factoryMethodToUse, argsToUse);
            }
            // 把bean对象放到包装类中
            bw.setBeanInstance(beanInstance);
            return bw;
        } catch (Throwable ex) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                    "Bean instantiation via factory method failed", ex);
        }
    }
}

public class SimpleInstantiationStrategy implements InstantiationStrategy {

    public Object instantiate(RootBeanDefinition bd, @Nullable String beanName, BeanFactory owner,
                              @Nullable Object factoryBean, final Method factoryMethod, @Nullable Object... args) {

        try {
            if (System.getSecurityManager() != null) {
                AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
                    ReflectionUtils.makeAccessible(factoryMethod);
                    return null;
                });
            } else {
                ReflectionUtils.makeAccessible(factoryMethod);
            }

            Method priorInvokedFactoryMethod = currentlyInvokedFactoryMethod.get();
            try {
                currentlyInvokedFactoryMethod.set(factoryMethod);
                // 调用工厂，创建bean
                Object result = factoryMethod.invoke(factoryBean, args);
                if (result == null) {
                    result = new NullBean();
                }
                return result;
            } finally {
                if (priorInvokedFactoryMethod != null) {
                    currentlyInvokedFactoryMethod.set(priorInvokedFactoryMethod);
                } else {
                    currentlyInvokedFactoryMethod.remove();
                }
            }
        } catch (IllegalArgumentException ex) {
            throw new BeanInstantiationException(factoryMethod,
                    "Illegal arguments to factory method '" + factoryMethod.getName() + "'; " +
                            "args: " + StringUtils.arrayToCommaDelimitedString(args), ex);
        } catch (IllegalAccessException ex) {
            throw new BeanInstantiationException(factoryMethod,
                    "Cannot access factory method '" + factoryMethod.getName() + "'; is it public?", ex);
        } catch (InvocationTargetException ex) {
            String msg = "Factory method '" + factoryMethod.getName() + "' threw exception";
            if (bd.getFactoryBeanName() != null && owner instanceof ConfigurableBeanFactory &&
                    ((ConfigurableBeanFactory) owner).isCurrentlyInCreation(bd.getFactoryBeanName())) {
                msg = "Circular reference involving containing bean '" + bd.getFactoryBeanName() + "' - consider " +
                        "declaring the factory method as static for independence from its containing instance. " + msg;
            }
            throw new BeanInstantiationException(factoryMethod, msg, ex.getTargetException());
        }
    }
}
```
