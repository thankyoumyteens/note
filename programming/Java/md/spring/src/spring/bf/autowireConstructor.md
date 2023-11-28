# 自动装配构造方法创建bean

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {

    protected BeanWrapper autowireConstructor(
            String beanName, RootBeanDefinition mbd, @Nullable Constructor<?>[] ctors, @Nullable Object[] explicitArgs) {

        return new ConstructorResolver(this).autowireConstructor(beanName, mbd, ctors, explicitArgs);
    }
}

class ConstructorResolver {

    /**
     * explicitArgs 从getBean()方法传入
     */
    public BeanWrapper autowireConstructor(String beanName, RootBeanDefinition mbd,
                                           @Nullable Constructor<?>[] chosenCtors, @Nullable Object[] explicitArgs) {

        BeanWrapperImpl bw = new BeanWrapperImpl();
        this.beanFactory.initBeanWrapper(bw);

        Constructor<?> constructorToUse = null;
        ArgumentsHolder argsHolderToUse = null;
        Object[] argsToUse = null;

        if (explicitArgs != null) {
            // 如果getBean()指定了参数, 则直接使用
            argsToUse = explicitArgs;
        } else {
            // 如果getBean()没有指定参数, 则试着从配置文件中获取
            Object[] argsToResolve = null;
            synchronized (mbd.constructorArgumentLock) {
                // 从缓存中获取已经解析过的构造方法
                constructorToUse = (Constructor<?>) mbd.resolvedConstructorOrFactoryMethod;
                // constructorArgumentsResolved=true表示构造方法参数已经解析
                // resolvedConstructorArguments和preparedConstructorArguments之中
                // 必然有一个缓存了构造方法参数
                if (constructorToUse != null && mbd.constructorArgumentsResolved) {
                    // 从缓存中获取已经解析的构造方法参数
                    argsToUse = mbd.resolvedConstructorArguments;
                    if (argsToUse == null) {
                        // 从缓存中获取准备用于解析的构造函数参数
                        argsToResolve = mbd.preparedConstructorArguments;
                    }
                }
            }
            if (argsToResolve != null) {
                // 转换参数类型
                // 缓存中渠道的参数类型不一定与构造方法的参数类型一致, 
                // 如果构造方法constructorToUse接收的参数类型是int, 
                // 而参数argsToUse中的参数类型是String(xml文件中解析出来的都是String), 
                // 则把argsToUse中的String转换成int类型
                argsToUse = resolvePreparedArguments(beanName, mbd, bw, constructorToUse, argsToResolve);
            }
        }

        if (constructorToUse == null) {
            // 缓存中没有构造方法, 则需要去解析构造方法
            // 判断是否传入了构造方法, 判断是否需要自动装配构造方法
            boolean autowiring = (chosenCtors != null ||
                    mbd.getResolvedAutowireMode() == AutowireCapableBeanFactory.AUTOWIRE_CONSTRUCTOR);
            // 用来存储已经解析的构造方法参数
            ConstructorArgumentValues resolvedValues = null;
            // 最小参数个数
            int minNrOfArgs;
            if (explicitArgs != null) {
                // 如果getBean()指定了参数
                minNrOfArgs = explicitArgs.length;
            } else {
                // 如果getBean()没有指定参数
                // cargs对象用来存放构造方法的参数
                ConstructorArgumentValues cargs = mbd.getConstructorArgumentValues();
                resolvedValues = new ConstructorArgumentValues();
                // 将BeanDefinition中配置的构造方法参数解析到resolvedValues中, 
                // 并返回构造方法参数的个数
                minNrOfArgs = resolveConstructorArguments(beanName, mbd, bw, cargs, resolvedValues);
            }

            // candidates存储候选的构造方法
            Constructor<?>[] candidates = chosenCtors;
            if (candidates == null) {
                // 没有传入构造方法
                // 获取bean的构造方法
                Class<?> beanClass = mbd.getBeanClass();
                try {
                    // 判断是否允许访问非public的构造方法
                    if (mbd.isNonPublicAccessAllowed()) {
                        // 允许, 则获取所有的构造方法
                        candidates = beanClass.getDeclaredConstructors();
                    } else {
                        // 不允许, 则只获取public的构造方法
                        candidates = beanClass.getConstructors();
                    }
                } catch (Throwable ex) {
                    throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                            "Resolution of declared constructors on bean Class [" + beanClass.getName() +
                                    "] from ClassLoader [" + beanClass.getClassLoader() + "] failed", ex);
                }
            }
            // 把候选的构造方法排序
            // 排序规则: 
            // 首先按照可访问性排序, public > protected > package > private
            // 如果可访问性相同, 则按照构造方法的参数个数由多到少排序
            AutowireUtils.sortConstructors(candidates);
            int minTypeDiffWeight = Integer.MAX_VALUE;
            Set<Constructor<?>> ambiguousConstructors = null;
            LinkedList<UnsatisfiedDependencyException> causes = null;
            // 遍历候选的构造方法, 寻找合适的构造方法
            for (Constructor<?> candidate : candidates) {
                // 获取候选构造方法的参数列表
                Class<?>[] paramTypes = candidate.getParameterTypes();
                // constructorToUse != null 表示找到了一个合适的构造方法, 
                // argsToUse.length > paramTypes.length 表示这个候选者的参数个数比目标少, 不匹配, 
                // 由于之前已经按照参数个数由多到少排序了, 所以后面的候选构造方法参数个数肯定比这个更少, 
                // 再继续遍历也不会有更合适的构造方法了, 可以跳出循环了
                if (constructorToUse != null && argsToUse.length > paramTypes.length) {
                    break;
                }
                // 候选者的参数个数比允许的最小个数的还少, 不匹配, 继续遍历
                if (paramTypes.length < minNrOfArgs) {
                    continue;
                }

                ArgumentsHolder argsHolder;
                if (resolvedValues != null) {
                    // 从BeanDefination中解析出了构造方法参数
                    try {
                        // 获取@ConstructorProperties注解中的配置的值
                        String[] paramNames = ConstructorPropertiesChecker.evaluate(candidate, paramTypes.length);
                        if (paramNames == null) {
                            // 没有@ConstructorProperties注解
                            // 获取候选者的参数名列表
                            ParameterNameDiscoverer pnd = this.beanFactory.getParameterNameDiscoverer();
                            if (pnd != null) {
                                paramNames = pnd.getParameterNames(candidate);
                            }
                        }
                        // 把候选者的参数列表封装到argsHolder对象里
                        argsHolder = createArgumentArray(beanName, mbd, resolvedValues, bw, paramTypes, paramNames,
                                getUserDeclaredConstructor(candidate), autowiring);
                    } catch (UnsatisfiedDependencyException ex) {
                        if (causes == null) {
                            causes = new LinkedList<>();
                        }
                        causes.add(ex);
                        continue;
                    }
                } else {
                    // 从BeanDefination中没有解析出构造方法参数
                    if (paramTypes.length != explicitArgs.length) {
                        // 候选者的参数个数与目标个数不一样
                        continue;
                    }
                    // 使用传进来的参数
                    argsHolder = new ArgumentsHolder(explicitArgs);
                }
                // 计算权重
                // isLenientConstructorResolution(): 判断解析构造方法使用宽松模式还是严格模式, 默认为宽松模式
                int typeDiffWeight = (mbd.isLenientConstructorResolution() ?
                        argsHolder.getTypeDifferenceWeight(paramTypes) : argsHolder.getAssignabilityWeight(paramTypes));
                // 根据权重找到最合适的构造方法
                if (typeDiffWeight < minTypeDiffWeight) {
                    constructorToUse = candidate;
                    argsHolderToUse = argsHolder;
                    argsToUse = argsHolder.arguments;
                    minTypeDiffWeight = typeDiffWeight;
                    ambiguousConstructors = null;
                } else if (constructorToUse != null && typeDiffWeight == minTypeDiffWeight) {
                    // 权重相同, 找到多个构造方法, 不知道该用哪个, 
                    // 记录下来, 后面用于抛异常
                    if (ambiguousConstructors == null) {
                        ambiguousConstructors = new LinkedHashSet<>();
                        ambiguousConstructors.add(constructorToUse);
                    }
                    ambiguousConstructors.add(candidate);
                }
            }

            if (constructorToUse == null) {
                // 没找到合适的构造方法, 抛异常
                if (causes != null) {
                    UnsatisfiedDependencyException ex = causes.removeLast();
                    for (Exception cause : causes) {
                        this.beanFactory.onSuppressedException(cause);
                    }
                    throw ex;
                }
                throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Could not resolve matching constructor " +
                                "(hint: specify index/type/name arguments for simple parameters to avoid type ambiguities)");
            } else if (ambiguousConstructors != null && !mbd.isLenientConstructorResolution()) {
                throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                        "Ambiguous constructor matches found in bean '" + beanName + "' " +
                                "(hint: specify index/type/name arguments for simple parameters to avoid type ambiguities): " +
                                ambiguousConstructors);
            }

            if (explicitArgs == null) {
                // 缓存解析的结果: 
                // 已解析出的构造方法对象resolvedConstructorOrFactoryMethod, 
                // 构造方法参数列表是否已解析标志constructorArgumentsResolved, 
                // 构造方法参数resolvedConstructorArguments或preparedConstructorArguments
                argsHolderToUse.storeCache(mbd, constructorToUse);
            }
        }

        try {
            final InstantiationStrategy strategy = beanFactory.getInstantiationStrategy();
            Object beanInstance;
            // 创建bean对象
            if (System.getSecurityManager() != null) {
                final Constructor<?> ctorToUse = constructorToUse;
                final Object[] argumentsToUse = argsToUse;
                beanInstance = AccessController.doPrivileged((PrivilegedAction<Object>) () ->
                                strategy.instantiate(mbd, beanName, beanFactory, ctorToUse, argumentsToUse),
                        beanFactory.getAccessControlContext());
            } else {
                beanInstance = strategy.instantiate(mbd, beanName, this.beanFactory, constructorToUse, argsToUse);
            }
            // 封装bean的包装类
            bw.setBeanInstance(beanInstance);
            return bw;
        } catch (Throwable ex) {
            throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                    "Bean instantiation via constructor failed", ex);
        }
    }
}

public class SimpleInstantiationStrategy implements InstantiationStrategy {

    public Object instantiate(RootBeanDefinition bd, @Nullable String beanName, BeanFactory owner,
                              final Constructor<?> ctor, @Nullable Object... args) {

        if (!bd.hasMethodOverrides()) {
            // 不需要替换方法
            if (System.getSecurityManager() != null) {
                // 校验权限
                AccessController.doPrivileged((PrivilegedAction<Object>) () -> {
                    ReflectionUtils.makeAccessible(ctor);
                    return null;
                });
            }
            // 调用有参或者无参的构造方法
            return (args != null ? BeanUtils.instantiateClass(ctor, args) : BeanUtils.instantiateClass(ctor));
        } else {
            // 需要替换方法
            // 这个方法会被子类CglibSubclassingInstantiationStrategy重写
            // 通过cglib动态代理实现方法的替换
            return instantiateWithMethodInjection(bd, beanName, owner, ctor, args);
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
