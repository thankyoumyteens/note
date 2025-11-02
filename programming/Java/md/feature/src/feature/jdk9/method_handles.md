# 方法句柄

Java 9 对方法句柄（Method Handles） 进行了进一步强化，主要体现在与模块化系统的适配、功能扩展以及与变量句柄（VarHandle）的协同上。方法句柄是 java.lang.invoke 包下的核心 API，用于动态访问和调用方法、构造器或字段，类似反射但性能更优，且支持更细粒度的访问控制。

## 模块化访问支持：privateLookupIn() 方法

ava 9 新增 `MethodHandles.privateLookupIn(Class<?> targetClass, MethodHandles.Lookup caller)` 方法，用于跨模块获取私有成员的方法句柄，解决了模块系统中私有成员访问的权限问题（替代了 Java 8 中受限的 lookup() 方法）。

跨模块访问私有方法:

```java
// User.java（模块 com.example.user）
// 需在 User 所在模块的 module-info.java 中开放权限:
// opens com.example.user to com.example.demo;
package com.example.user;
public class User {
    private String getSecret() {
        return "secret";
    }
}

// Demo.java（模块 com.example.demo）
package com.example.demo;
import com.example.user.User;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodType;

public class Demo {
    public static void main(String[] args) throws Throwable {
        // 1. 获取调用者的 Lookup 对象
        MethodHandles.Lookup caller = MethodHandles.lookup();

        // 2. 跨模块获取 User 类的私有访问句柄
        MethodHandles.Lookup privateLookup = MethodHandles.privateLookupIn(User.class, caller);

        // 3. 查找私有方法 getSecret()（无参数，返回 String）
        MethodHandle getSecretHandle = privateLookup.findVirtual(
            User.class,
            "getSecret",
            MethodType.methodType(String.class)
        );

        // 4. 调用方法句柄（等价于 user.getSecret()）
        User user = new User();
        String secret = (String) getSecretHandle.invoke(user);
        System.out.println(secret); // 输出：secret
    }
}
```

## 方法句柄的组合与转换增强

Java 9 扩展了方法句柄的组合能力，通过 MethodHandle 的静态方法可更灵活地拼接、适配方法调用：

- MethodHandle.filterArguments()：对方法的输入参数进行过滤转换。
- MethodHandle.filterReturnValue()：对方法的返回值进行过滤转换。
- MethodHandle.compose()/andThen()：将多个方法句柄串联成调用链（类似函数式编程的 compose 和 andThen）。

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodType;

public class MethodHandleDemo {
    public static void main(String[] args) throws Throwable {
        // 1. 获取字符串转整数的方法句柄（Integer.parseInt(String)）
        MethodHandle parseInt = MethodHandles.lookup()
            .findStatic(Integer.class, "parseInt", MethodType.methodType(int.class, String.class));

        // 2. 获取整数加 10 的方法句柄（自定义方法）
        MethodHandle add10 = MethodHandles.lookup()
            .findStatic(MethodHandleDemo.class, "add10", MethodType.methodType(int.class, int.class));

        // 3. 组合：先 parseInt，再 add10（等价于 add10(parseInt(s))）
        MethodHandle combined = add10.compose(parseInt);

        // 调用组合句柄
        int result = (int) combined.invoke("123"); // "123" -> 123 -> 133
        System.out.println(result); // 输出：133
    }

    private static int add10(int num) {
        return num + 10;
    }
}
```
