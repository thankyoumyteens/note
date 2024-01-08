# CGLIB 动态代理

## 用法

1. maven 依赖

```xml
<dependency>
    <groupId>cglib</groupId>
    <artifactId>cglib</artifactId>
    <version>3.3.0</version>
</dependency>
```

2. 被代理类

```java
package org.example;

public class DemoCGLib {
    public void call() {
        System.out.println("ok");
    }
}
```

3. 代理方法

```java
package org.example;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;
import java.lang.reflect.Method;

public class DemoProxy implements MethodInterceptor {
    public Object intercept(Object o, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
        System.out.println("pre");
        // 调用被代理类的方法
        Object returnValue = methodProxy.invokeSuper(o, args);
        System.out.println("post");
        return returnValue;
    }
}
```

4. 使用动态代理

```java
package org.example;
import net.sf.cglib.core.DebuggingClassWriter;
import net.sf.cglib.proxy.Enhancer;

public class App {
    public static void main(String[] args) {
        Enhancer enhancer = new Enhancer();
        // 被代理类
        enhancer.setSuperclass(DemoCGLib.class);
        enhancer.setCallback(new DemoProxy());
        DemoCGLib proxyInstance = (DemoCGLib) enhancer.create();
        proxyInstance.call();
    }
}
```

5. 输出

```
pre
ok
post
```

## 把动态生成的代理类保存到磁盘

在程序入口加下下面一行:

```java
package org.example;
import net.sf.cglib.core.DebuggingClassWriter;
import net.sf.cglib.proxy.Enhancer;

public class App {
    public static void main(String[] args) {
        // 指定 CGLIB 将动态生成的代理类保存至指定的磁盘路径下
        System.setProperty(DebuggingClassWriter.DEBUG_LOCATION_PROPERTY, "C:\\Users\\Public\\cglib_output");

        Enhancer enhancer = new Enhancer();
        // 被代理类
        enhancer.setSuperclass(DemoCGLib.class);
        enhancer.setCallback(new DemoProxy());
        DemoCGLib proxyInstance = (DemoCGLib) enhancer.create();
        proxyInstance.call();
    }
}
```

重新运行程序后, 可以看到生成的代理类:

![](./img/generated_cglib_class.png)
