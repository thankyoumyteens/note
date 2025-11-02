# 变量句柄

Java 9 引入的变量句柄（Variable Handles） 是位于 java.lang.invoke 包下的一组 API（核心类为 VarHandle），旨在提供一种更灵活、高效且安全的方式来访问和操作对象字段、数组元素或静态变量，替代了传统的 sun.misc.Unsafe 类的部分功能（如原子更新、内存屏障），同时提供更强的类型安全和平台兼容性。

## VarHandle 类

VarHandle 是所有变量句柄的父类，代表对一个变量（字段、数组元素、静态变量）的引用。通过它可以执行以下操作：

- 读取 / 写入变量（get()/set()）。
- 原子更新操作（compareAndSet()、getAndAdd() 等）。
- 带有内存排序约束的操作（控制多线程下的可见性和顺序性）。

变量句柄支持多种内存排序模式（通过方法后缀区分），对应不同的并发语义，常见模式包括：

- plain：普通访问，无内存排序约束（等价于非 volatile 变量的默认访问）。
- volatile：volatile 语义，保证读写的可见性和顺序性（等价于 volatile 变量）。
- acquire：读操作时，后续读写不能重排序到该操作之前（获取锁的语义）。
- release：写操作时，之前的读写不能重排序到该操作之后（释放锁的语义）。
- opaque：不保证可见性，但禁止编译器和 CPU 重排序（仅保证操作本身的原子性）。

## 访问对象字段

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

class User {
    private String name; // 私有字段
    public int age;     // 公共字段

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

public class VarHandleDemo {
    public static void main(String[] args) throws NoSuchFieldException, IllegalAccessException {
        // 获取 User 类的 name 字段的 VarHandle
        // 1. 获取调用者的 Lookup 对象（代表当前类的访问权限）
        MethodHandles.Lookup caller = MethodHandles.lookup();
        // 2. 使用 privateLookupIn 获取目标类 User 的私有访问句柄
        MethodHandles.Lookup privateLookup = MethodHandles.privateLookupIn(User.class, caller);
        // 3. 通过私有访问句柄获取 User.name 字段的 VarHandle
        VarHandle nameHandle = privateLookup.findVarHandle(User.class, "name", String.class);

        // 获取 User 类的 age 字段的 VarHandle
        VarHandle ageHandle = MethodHandles.lookup()
                .findVarHandle(User.class, "age", int.class);

        User user = new User("Alice", 20);

        // 读取字段（plain 模式）
        String name = (String) nameHandle.get(user);
        int age = (int) ageHandle.get(user);
        System.out.println("原始值：" + name + ", " + age); // 输出：Alice, 20

        // 修改字段（plain 模式）
        nameHandle.set(user, "Bob");
        ageHandle.set(user, 25);
        // 输出：Bob, 25
        System.out.println("修改后：" + nameHandle.get(user) + ", " + ageHandle.get(user));

        // 原子更新 age（compareAndSet：如果当前值为 25，则更新为 30）
        boolean success = ageHandle.compareAndSet(user, 25, 30);
        // 输出：true, 30
        System.out.println("原子更新成功？" + success + "，新值：" + ageHandle.get(user));
    }
}
```

## 访问数组元素

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

public class ArrayVarHandleDemo {
    public static void main(String[] args) {
        // 获取 int 数组元素的 VarHandle
        VarHandle intArrayHandle = MethodHandles.arrayElementVarHandle(int[].class);

        int[] array = {10, 20, 30};

        // 读取数组元素（volatile 模式，保证可见性）
        int value = (int) intArrayHandle.getVolatile(array, 1);
        System.out.println("数组[1]原始值：" + value); // 输出：20

        // 原子自增（getAndAdd：先获取当前值，再加上 5）
        int oldValue = (int) intArrayHandle.getAndAdd(array, 1, 5);
        System.out.println("数组[1]自增前：" + oldValue + "，自增后：" + array[1]); // 输出：20, 25
    }
}
```
