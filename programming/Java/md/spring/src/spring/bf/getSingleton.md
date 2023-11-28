# 从缓存中获取单例bean

单例在Spring的同一个容器内只会被创建一次, 后续再获取bean直接从单例缓存中获取。

```java
public class DefaultSingletonBeanRegistry extends SimpleAliasRegistry implements SingletonBeanRegistry {

    public Object getSingleton(String beanName) {
        return getSingleton(beanName, true);
    }

    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
        // singletonObjects就是单例缓存
        Object singletonObject = this.singletonObjects.get(beanName);
        // 缓存里没有, isSingletonCurrentlyInCreation()用于解决循环依赖
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            // 下面的代码用于解决循环依赖
            synchronized (this.singletonObjects) {
                singletonObject = this.earlySingletonObjects.get(beanName);
                if (singletonObject == null && allowEarlyReference) {
                    
                    ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                    if (singletonFactory != null) {
                        singletonObject = singletonFactory.getObject();
                        this.earlySingletonObjects.put(beanName, singletonObject);
                        this.singletonFactories.remove(beanName);
                    }
                }
            }
        }
        return singletonObject;
    }
}
```
