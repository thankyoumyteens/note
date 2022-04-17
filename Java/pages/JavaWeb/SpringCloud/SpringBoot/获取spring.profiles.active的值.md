```java
@Component
public class SpringContextUtil implements ApplicationContextAware {
 
    private static ApplicationContext context = null;
 
    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.context = applicationContext;
    }
 
    /// 获取当前环境
    public static String getActiveProfile() {
        return context.getEnvironment().getActiveProfiles()[0];
    }
}
```
