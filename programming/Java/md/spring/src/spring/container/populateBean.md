# 填充 bean 属性

```java
public abstract class AbstractAutowireCapableBeanFactory extends AbstractBeanFactory
        implements AutowireCapableBeanFactory {
    
    /**
     * 填充bean属性
     */
    protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
        if (bw == null) {
            if (mbd.hasPropertyValues()) {
                throw new BeanCreationException(
                        mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance");
            } else {
                // 没有属性需要填充，直接返回
                return;
            }
        }

        if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
            // 执行InstantiationAwareBeanPostProcessor后置处理器
            for (BeanPostProcessor bp : getBeanPostProcessors()) {
                if (bp instanceof InstantiationAwareBeanPostProcessor) {
                    // 后置处理器可能返回一个代理对象取代原有的bean
                    InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
                    if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
                        return;
                    }
                }
            }
        }

        PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);
        // 获取自动装配类型
        int resolvedAutowireMode = mbd.getResolvedAutowireMode();
        if (resolvedAutowireMode == AUTOWIRE_BY_NAME || resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
            MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
            // byName，找出和字段名相同的bean，存入newPvs中
            if (resolvedAutowireMode == AUTOWIRE_BY_NAME) {
                autowireByName(beanName, mbd, bw, newPvs);
            }
            // byType，找出和字段类型相同的bean，存入newPvs中
            if (resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
                autowireByType(beanName, mbd, bw, newPvs);
            }
            pvs = newPvs;
        }
        // 判断InstantiationAwareBeanPostProcessor后置处理器是否已经初始化
        boolean hasInstAwareBpps = hasInstantiationAwareBeanPostProcessors();
        // 是否需要依赖检查
        boolean needsDepCheck = (mbd.getDependencyCheck() != AbstractBeanDefinition.DEPENDENCY_CHECK_NONE);

        if (hasInstAwareBpps || needsDepCheck) {
            if (pvs == null) {
                pvs = mbd.getPropertyValues();
            }
            // 过滤出需要依赖检查的属性
            PropertyDescriptor[] filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
            if (hasInstAwareBpps) {
                for (BeanPostProcessor bp : getBeanPostProcessors()) {
                    if (bp instanceof InstantiationAwareBeanPostProcessor) {
                        // 对需要依赖检查的属性执行后置处理器
                        InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
                        pvs = ibp.postProcessPropertyValues(pvs, filteredPds, bw.getWrappedInstance(), beanName);
                        if (pvs == null) {
                            return;
                        }
                    }
                }
            }
            // 执行依赖检查
            if (needsDepCheck) {
                checkDependencies(beanName, mbd, filteredPds, pvs);
            }
        }

        if (pvs != null) {
            // 把pvs中的属性填充到BeanWrapper中
            applyPropertyValues(beanName, mbd, bw, pvs);
        }
    }

    /**
     * byName
     */
    protected void autowireByName(
            String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {
        // 获取bw中需要依赖注入的属性列表
        String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
        for (String propertyName : propertyNames) {
            // 只有bean需要注入
            if (containsBean(propertyName)) {
                // 创建bean
                Object bean = getBean(propertyName);
                // 把属性存入pvs中
                pvs.add(propertyName, bean);
                // 注册propertyName和beanName的依赖关系
                // 实现在销毁propertyName指向的bean之前先把beanName指向的bean销毁
                registerDependentBean(propertyName, beanName);
            }
        }
    }

    /**
     * byType
     */
    protected void autowireByType(
            String beanName, AbstractBeanDefinition mbd, BeanWrapper bw, MutablePropertyValues pvs) {

        TypeConverter converter = getCustomTypeConverter();
        if (converter == null) {
            converter = bw;
        }

        Set<String> autowiredBeanNames = new LinkedHashSet<>(4);
        // 获取bw中需要依赖注入的属性列表
        String[] propertyNames = unsatisfiedNonSimpleProperties(mbd, bw);
        for (String propertyName : propertyNames) {
            try {
                PropertyDescriptor pd = bw.getPropertyDescriptor(propertyName);
                if (Object.class != pd.getPropertyType()) {
                    // 查找指定属性的setter
                    MethodParameter methodParam = BeanUtils.getWriteMethodParameter(pd);
                    boolean eager = !(bw.getWrappedInstance() instanceof PriorityOrdered);
                    DependencyDescriptor desc = new AutowireByTypeDependencyDescriptor(methodParam, eager);
                    // 寻找与属性类型匹配的bean
                    Object autowiredArgument = resolveDependency(desc, beanName, autowiredBeanNames, converter);
                    if (autowiredArgument != null) {
                        // 把属性存入pvs中
                        pvs.add(propertyName, autowiredArgument);
                    }
                    for (String autowiredBeanName : autowiredBeanNames) {
                        // 注册autowiredBeanName和beanName的依赖关系
                        registerDependentBean(autowiredBeanName, beanName);
                    }
                    autowiredBeanNames.clear();
                }
            } catch (BeansException ex) {
                throw new UnsatisfiedDependencyException(mbd.getResourceDescription(), beanName, propertyName, ex);
            }
        }
    }

    protected void applyPropertyValues(String beanName, BeanDefinition mbd, BeanWrapper bw, PropertyValues pvs) {
        if (pvs.isEmpty()) {
            return;
        }

        if (System.getSecurityManager() != null && bw instanceof BeanWrapperImpl) {
            ((BeanWrapperImpl) bw).setSecurityContext(getAccessControlContext());
        }

        MutablePropertyValues mpvs = null;
        List<PropertyValue> original;

        if (pvs instanceof MutablePropertyValues) {
            mpvs = (MutablePropertyValues) pvs;
            if (mpvs.isConverted()) {
                // Shortcut: use the pre-converted values as-is.
                try {
                    bw.setPropertyValues(mpvs);
                    return;
                } catch (BeansException ex) {
                    throw new BeanCreationException(
                            mbd.getResourceDescription(), beanName, "Error setting property values", ex);
                }
            }
            original = mpvs.getPropertyValueList();
        } else {
            original = Arrays.asList(pvs.getPropertyValues());
        }

        TypeConverter converter = getCustomTypeConverter();
        if (converter == null) {
            converter = bw;
        }
        BeanDefinitionValueResolver valueResolver = new BeanDefinitionValueResolver(this, beanName, mbd, converter);

        // Create a deep copy, resolving any references for values.
        List<PropertyValue> deepCopy = new ArrayList<>(original.size());
        boolean resolveNecessary = false;
        for (PropertyValue pv : original) {
            if (pv.isConverted()) {
                deepCopy.add(pv);
            } else {
                String propertyName = pv.getName();
                Object originalValue = pv.getValue();
                Object resolvedValue = valueResolver.resolveValueIfNecessary(pv, originalValue);
                Object convertedValue = resolvedValue;
                boolean convertible = bw.isWritableProperty(propertyName) &&
                        !PropertyAccessorUtils.isNestedOrIndexedProperty(propertyName);
                if (convertible) {
                    convertedValue = convertForProperty(resolvedValue, propertyName, bw, converter);
                }
                // Possibly store converted value in merged bean definition,
                // in order to avoid re-conversion for every created bean instance.
                if (resolvedValue == originalValue) {
                    if (convertible) {
                        pv.setConvertedValue(convertedValue);
                    }
                    deepCopy.add(pv);
                } else if (convertible && originalValue instanceof TypedStringValue &&
                        !((TypedStringValue) originalValue).isDynamic() &&
                        !(convertedValue instanceof Collection || ObjectUtils.isArray(convertedValue))) {
                    pv.setConvertedValue(convertedValue);
                    deepCopy.add(pv);
                } else {
                    resolveNecessary = true;
                    deepCopy.add(new PropertyValue(pv, convertedValue));
                }
            }
        }
        if (mpvs != null && !resolveNecessary) {
            mpvs.setConverted();
        }

        // Set our (possibly massaged) deep copy.
        try {
            bw.setPropertyValues(new MutablePropertyValues(deepCopy));
        } catch (BeansException ex) {
            throw new BeanCreationException(
                    mbd.getResourceDescription(), beanName, "Error setting property values", ex);
        }
    }
}

public class DefaultListableBeanFactory extends AbstractAutowireCapableBeanFactory
        implements ConfigurableListableBeanFactory, BeanDefinitionRegistry, Serializable {

    public Object resolveDependency(DependencyDescriptor descriptor, @Nullable String requestingBeanName,
                                    @Nullable Set<String> autowiredBeanNames, @Nullable TypeConverter typeConverter) throws BeansException {

        descriptor.initParameterNameDiscovery(getParameterNameDiscoverer());
        if (Optional.class == descriptor.getDependencyType()) {
            return createOptionalDependency(descriptor, requestingBeanName);
        } else if (ObjectFactory.class == descriptor.getDependencyType() ||
                ObjectProvider.class == descriptor.getDependencyType()) {
            return new DependencyObjectProvider(descriptor, requestingBeanName);
        } else if (javaxInjectProviderClass == descriptor.getDependencyType()) {
            return new Jsr330ProviderFactory().createDependencyProvider(descriptor, requestingBeanName);
        } else {
            Object result = getAutowireCandidateResolver().getLazyResolutionProxyIfNecessary(
                    descriptor, requestingBeanName);
            if (result == null) {
                result = doResolveDependency(descriptor, requestingBeanName, autowiredBeanNames, typeConverter);
            }
            return result;
        }
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

            Object multipleBeans = resolveMultipleBeans(descriptor, beanName, autowiredBeanNames, typeConverter);
            if (multipleBeans != null) {
                return multipleBeans;
            }

            Map<String, Object> matchingBeans = findAutowireCandidates(beanName, type, descriptor);
            if (matchingBeans.isEmpty()) {
                if (isRequired(descriptor)) {
                    raiseNoMatchingBeanFound(type, descriptor.getResolvableType(), descriptor);
                }
                return null;
            }

            String autowiredBeanName;
            Object instanceCandidate;

            if (matchingBeans.size() > 1) {
                autowiredBeanName = determineAutowireCandidate(matchingBeans, descriptor);
                if (autowiredBeanName == null) {
                    if (isRequired(descriptor) || !indicatesMultipleBeans(type)) {
                        return descriptor.resolveNotUnique(type, matchingBeans);
                    } else {
                        // In case of an optional Collection/Map, silently ignore a non-unique case:
                        // possibly it was meant to be an empty collection of multiple regular beans
                        // (before 4.3 in particular when we didn't even look for collection beans).
                        return null;
                    }
                }
                instanceCandidate = matchingBeans.get(autowiredBeanName);
            } else {
                // We have exactly one match.
                Map.Entry<String, Object> entry = matchingBeans.entrySet().iterator().next();
                autowiredBeanName = entry.getKey();
                instanceCandidate = entry.getValue();
            }

            if (autowiredBeanNames != null) {
                autowiredBeanNames.add(autowiredBeanName);
            }
            if (instanceCandidate instanceof Class) {
                instanceCandidate = descriptor.resolveCandidate(autowiredBeanName, type, this);
            }
            Object result = instanceCandidate;
            if (result instanceof NullBean) {
                if (isRequired(descriptor)) {
                    raiseNoMatchingBeanFound(type, descriptor.getResolvableType(), descriptor);
                }
                result = null;
            }
            if (!ClassUtils.isAssignableValue(type, result)) {
                throw new BeanNotOfRequiredTypeException(autowiredBeanName, type, instanceCandidate.getClass());
            }
            return result;
        } finally {
            ConstructorResolver.setCurrentInjectionPoint(previousInjectionPoint);
        }
    }
}
```
