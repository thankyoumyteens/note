# 初始化 bean

Spring 为 bean 提供了两种初始化 bean 的方式, 实现 InitializingBean 接口或者通过在 XML 配置文件中添加 init-method 的方式, 这两种方式可以同时使用。如果 bean 实现了 InitializingBean 接口, 并且同时在配置文件中指定了 init-method, Spring 会先调用 afterPropertiesSet 方法, 然后再调用 init-method 中指定的方法。

实现 InitializingBean 接口是直接调用 afterPropertiesSet 方法, 比通过反射调用 init-method 指定的方法效率要高一点, 但是 init-method 方式消除了对 spring 的依赖。如果调用 afterPropertiesSet 方法时出错, 则不调用 init-method 指定的方法。

## InitializingBean

InitializingBean 是 Spring 提供的拓展性接口, InitializingBean 接口为 bean 提供了属性初始化后的处理方法, 它只有一个 afterPropertiesSet 方法, 凡是实现该接口的类, 在 bean 的属性初始化后都会执行该方法。

```java
@Component
public class MyInitializingBean implements InitializingBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("自定义初始化");
    }
}
```

## init-method

通过 XML 文件方式配置 init-method 方法: 

```xml
<bean id="myBean" class="test.MyBean" init-method="myInit" />
```

通过@Bean 的方式配置 init-method 方法: 

```java
@Bean(initMethod = "myInit")
public MyBean myBean() {
    return new MyBean();
}
```
