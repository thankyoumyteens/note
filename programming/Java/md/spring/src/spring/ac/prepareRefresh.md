# 准备工作

prepareRefresh()方法主要是做些准备工作, 例如对系统属性及环境变量的初始化及验证。

```java
public abstract class AbstractApplicationContext extends DefaultResourceLoader
        implements ConfigurableApplicationContext {

    protected void prepareRefresh() {
        this.startupDate = System.currentTimeMillis();
        this.closed.set(false);
        this.active.set(true);

        // 留给子类实现, 子类可以在environment中添加自定义属性
        initPropertySources();

        // 验证environment中的属性
        getEnvironment().validateRequiredProperties();

        if (this.earlyApplicationListeners == null) {
            this.earlyApplicationListeners = new LinkedHashSet<>(this.applicationListeners);
        } else {
            this.applicationListeners.clear();
            this.applicationListeners.addAll(this.earlyApplicationListeners);
        }

        this.earlyApplicationEvents = new LinkedHashSet<>();
    }
}
```
