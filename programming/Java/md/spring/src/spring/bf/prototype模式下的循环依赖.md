# prototype模式下的循环依赖

spring无法解决prototype模式下的循环依赖, 如果发现循环依赖, 会直接抛出异常。

```java
public class TestA {
    @Resource
    private TestB testB;
}

public class TestB {
    @Resource
    private TestA testA;
}

TestA a = (TestA) bf.getBean("testA");
```

此时prototype模式下getBean的执行过程: 

1. 检查prototypesCurrentlyInCreation中是否记录了testA, 由于testA是第一次创建, 所以没有记录
2. 把testA记录到prototypesCurrentlyInCreation中
2. 创建testA, 并执行依赖注入
3. spring发现testA中依赖了testB, 会调用getBean()方法获取testB
4. 由于testB没有创建, 所以也会开始执行创建过程
5. 首先检查prototypesCurrentlyInCreation中是否记录了testB, 由于testB是第一次创建, 所以没有记录
6. 把testB记录到prototypesCurrentlyInCreation中
7. 创建testB, 并执行依赖注入
8. 这时, spring发现testB中依赖了testA, 会调用getBean()方法获取testA
9. testA此时还没创建玩, getBean()获取不到testA, 会执行新的创建过程
10. 检查prototypesCurrentlyInCreation中是否记录了testA, 此时testA已经被记录, spring发现这时循环引用, 抛出异常

```java
public abstract class AbstractBeanFactory extends FactoryBeanRegistrySupport implements ConfigurableBeanFactory {

    // 保存prototype模式下正在创建的beanName
    private final ThreadLocal<Object> prototypesCurrentlyInCreation =
            new NamedThreadLocal<>("Prototype beans currently in creation");

    // getBean
    protected <T> T doGetBean(String name, @Nullable Class<T> requiredType, @Nullable Object[] args, boolean typeCheckOnly)
            throws BeansException {

        String beanName = transformedBeanName(name);
        Object bean;

        if (sharedInstance != null && args == null) {
            // ...
        } else {
            // 检查prototypesCurrentlyInCreation中是否记录了beanName
            if (isPrototypeCurrentlyInCreation(beanName)) {
                // 循环引用, 抛出异常
                throw new BeanCurrentlyInCreationException(beanName);
            }
            // ...
            try {
                RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
                // 实例化bean
                if (mbd.isSingleton()) {
                    // ...
                } else if (mbd.isPrototype()) {
                    // prototype模式
                    Object prototypeInstance = null;
                    try {
                        // 把beanName记录prototypesCurrentlyInCreation, 表示正在创建, 还没创建完
                        beforePrototypeCreation(beanName);
                        // 创建bean, 里面会执行依赖注入
                        prototypeInstance = createBean(beanName, mbd, args);
                    } finally {
                        // 创建完了, 把beanName从prototypesCurrentlyInCreation中删掉
                        afterPrototypeCreation(beanName);
                    }
                    bean = getObjectForBeanInstance(prototypeInstance, name, beanName, mbd);
                } else {
                    // ...
                }
            } catch (BeansException ex) {
                // ...
            }
        }
        // ...
        return (T) bean;
    }

    // 判断beanName在不在prototypesCurrentlyInCreation中
    protected boolean isPrototypeCurrentlyInCreation(String beanName) {
        Object curVal = this.prototypesCurrentlyInCreation.get();
        return (curVal != null &&
                (curVal.equals(beanName) || (curVal instanceof Set && ((Set<?>) curVal).contains(beanName))));
    }

    // 把beanName记录到prototypesCurrentlyInCreation中
    protected void beforePrototypeCreation(String beanName) {
        // 只有1个beanName时, prototypesCurrentlyInCreation用一个字符串存储它, 
        // 当第2个beanName加进来时, 一个字符串无法存储两个beanName了, 
        // 因此需要把prototypesCurrentlyInCreation转换成Set
        Object curVal = this.prototypesCurrentlyInCreation.get();
        if (curVal == null) {
            this.prototypesCurrentlyInCreation.set(beanName);
        } else if (curVal instanceof String) {
            // String升级成Set
            Set<String> beanNameSet = new HashSet<>(2);
            beanNameSet.add((String) curVal);
            beanNameSet.add(beanName);
            this.prototypesCurrentlyInCreation.set(beanNameSet);
        } else {
            Set<String> beanNameSet = (Set<String>) curVal;
            beanNameSet.add(beanName);
        }
    }

    // 把beanName从prototypesCurrentlyInCreation中删除
    protected void afterPrototypeCreation(String beanName) {
        Object curVal = this.prototypesCurrentlyInCreation.get();
        if (curVal instanceof String) {
            this.prototypesCurrentlyInCreation.remove();
        } else if (curVal instanceof Set) {
            Set<String> beanNameSet = (Set<String>) curVal;
            beanNameSet.remove(beanName);
            if (beanNameSet.isEmpty()) {
                this.prototypesCurrentlyInCreation.remove();
            }
        }
    }
}
```
