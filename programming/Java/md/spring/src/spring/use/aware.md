# Aware 接口

Spring 的依赖注入的最大亮点是所有的 Bean 对 Spring 容器的存在是没有感知的，Spring 容器中的 Bean 的耦合度因此也是极低的。但是在实际的开发中，经常要用到 Spring 容器本身的功能，所以 Spring 容器中的 Bean 此时就要感知到 Spring 容器的存在才能调用 Spring 所提供的功能。Spring 提供了 Aware 来实现这个功能。

若 Spring 检测到 bean 实现了 Aware 接口，则会为其注入相应的依赖。所以通过让 bean 实现 Aware 接口，则能在 bean 中获得相应的 Spring 容器资源。

常见的Aware：

- BeanNameAware：获得到容器中Bean的名称
- ApplicationContextAware：获得当前的ApplicationContext对象
- ResourceLoaderAware：获取资源加载器，可以获得外部资源文件

## 使用ApplicationContextAware

```java
@Component
public class SpringUtil implements ApplicationContextAware {

    private static ApplicationContext ac;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.ac = applicationContext;
    }

    /**
     * 在不方便使用@Autowired注解时，可以使用此方法获得Bean
     */
    public static <T> T getBean(Class<T> type) {
        return (T) ac.getBean(type);
    }
}
```
