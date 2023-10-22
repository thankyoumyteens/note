# 注册BeanDefinition

bean标签解析完成后，spring会把解析好的BeanDefinition对象注册到BeanDefinitionRegistry中。

BeanDefinitionRegistry是一个注册中心，所有的BeanDefinition都会注册到它上面。想要获取BeanDefinition的时候，就可以通过beanName从这个注册中心获取。


```java
public class BeanDefinitionReaderUtils {

    /**
     * 注册BeanDefinition
     * 这里传入的registry是BeanDefinitionRegistry的实现类：DefaultListableBeanFactory
     */
    public static void registerBeanDefinition(
            BeanDefinitionHolder definitionHolder, BeanDefinitionRegistry registry)
            throws BeanDefinitionStoreException {

        // 使用beanName作为唯一标识注册
        String beanName = definitionHolder.getBeanName();
        registry.registerBeanDefinition(beanName, definitionHolder.getBeanDefinition());

        // 注册所有的别名
        String[] aliases = definitionHolder.getAliases();
        if (aliases != null) {
            for (String alias : aliases) {
                registry.registerAlias(beanName, alias);
            }
        }
    }
}
```

## 使用beanName注册bean

```java
public class DefaultListableBeanFactory extends AbstractAutowireCapableBeanFactory
        implements ConfigurableListableBeanFactory, BeanDefinitionRegistry, Serializable {
    
    public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
            throws BeanDefinitionStoreException {

        if (beanDefinition instanceof AbstractBeanDefinition) {
            try {
                // 注册前的最后一次校验，这里的校验不同于之前的XML文件校验，
                // 主要是对于AbstractBeanDefinition中的methodOverrides的校验 
                // 校验methodOverrides是否与工厂方法并存
                // 或者methodOverrides对应的方法根本不存在
                ((AbstractBeanDefinition) beanDefinition).validate();
            } catch (BeanDefinitionValidationException ex) {
                throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
                        "Validation of bean definition failed", ex);
            }
        }

        // 所有bean都在一个全局的map中
        // 查找beanName是否已存在
        BeanDefinition existingDefinition = this.beanDefinitionMap.get(beanName);
        if (existingDefinition != null) {
            // beanName在map中
            if (!isAllowBeanDefinitionOverriding()) {
                // 如果不允许覆盖旧的bean，则抛异常
                throw new BeanDefinitionStoreException(beanDefinition.getResourceDescription(), beanName,
                        "Cannot register bean definition [" + beanDefinition + "] for bean '" + beanName +
                        "': There is already [" + existingDefinition + "] bound.");
            }
            // 把beanName作为key，beanDefinition作为value，存储到map中
            this.beanDefinitionMap.put(beanName, beanDefinition);
        } else {
            // beanName不在map中
            // 判断是不是已经有bean被创建
            // 如果已经有bean被创建，那么代表已经开始进行了业务操作，
            // Spring容器无法保证下面的代码不会出现线程安全问题，所以需要加锁
            if (hasBeanCreationStarted()) {
                synchronized (this.beanDefinitionMap) {
                    // 把beanName作为key，beanDefinition作为value，存储到map中
                    this.beanDefinitionMap.put(beanName, beanDefinition);
                    // 维护beanName的列表
                    List<String> updatedDefinitions = new ArrayList<>(this.beanDefinitionNames.size() + 1);
                    updatedDefinitions.addAll(this.beanDefinitionNames);
                    updatedDefinitions.add(beanName);
                    this.beanDefinitionNames = updatedDefinitions;
                    if (this.manualSingletonNames.contains(beanName)) {
                        Set<String> updatedSingletons = new LinkedHashSet<>(this.manualSingletonNames);
                        updatedSingletons.remove(beanName);
                        this.manualSingletonNames = updatedSingletons;
                    }
                }
            } else {
                // 还处在spring容器的启动阶段，不用加锁
                this.beanDefinitionMap.put(beanName, beanDefinition);
                this.beanDefinitionNames.add(beanName);
                this.manualSingletonNames.remove(beanName);
            }
            this.frozenBeanDefinitionNames = null;
        }
        // 重置所有beanName对应的缓存
        if (existingDefinition != null || containsSingleton(beanName)) {
            resetBeanDefinition(beanName);
        } else if (isConfigurationFrozen()) {
            clearByTypeCache();
        }
    }
}
```

## 使用别名注册bean

```java
public class SimpleAliasRegistry implements AliasRegistry {

    public void registerAlias(String name, String alias) {
        synchronized (this.aliasMap) {
            if (alias.equals(name)) {
                // 别名和beanName一样，删掉
                this.aliasMap.remove(alias);
            } else {
                String registeredName = this.aliasMap.get(alias);
                if (registeredName != null) {
                    // 这个bean已经注册过这个别名了
                    if (registeredName.equals(name)) {
                        return;
                    }
                    // 是否允许覆盖旧值
                    if (!allowAliasOverriding()) {
                        throw new IllegalStateException("Cannot define alias '" + alias + "' for name '" +
                                name + "': It is already registered for name '" + registeredName + "'.");
                    }
                }
                // 当A->B存在时，如果再出现A->C->B，就会抛异常
                checkForAliasCircle(name, alias);
                // 注册别名
                this.aliasMap.put(alias, name);
            }
        }
    }
}
```
