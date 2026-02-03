# ASM动态生成的类使用EasyExcel导出报错NoClassDefFoundError

大概是这样的场景：

- 你有一个 **自定义 ClassLoader**，用来加载 ASM 动态生成的类；
- 项目里还用了 **EasyExcel** 做导出；
- 一旦导出时用到这些动态类，就报 `ClassNotFoundException` / `NoClassDefFoundError` 类似错误。

## 错误原因

这种问题，本质上的原因都是：**类是你用自定义 ClassLoader 加进来的，但 EasyExcel 所在的 ClassLoader 并不知道它们**。

### 1. 自定义 ClassLoader 没有设置成上下文类加载器（ContextClassLoader）

很多框架（包括 EasyExcel、Spring、一些反射工具）默认是用：

```java
Thread.currentThread().getContextClassLoader()
```

来加载类的，而不是 `SomeClass.class.getClassLoader()`。

如果你只是 `new MyDynamicClassLoader(...)` 然后自己 `loader.defineClass(...)`，但是 **没有把它设置为当前线程的 ContextClassLoader**，那么 EasyExcel 仍然会用原来的那个 classloader，自然找不到你刚动态生成的类。

### 2. EasyExcel 运行的线程和你设置 ContextClassLoader 的线程不是同一个

比如：

1. 你在主线程上设置了：
   ```java
   Thread.currentThread().setContextClassLoader(dynamicClassLoader);
   ```
2. 但实际导出是在线程池、异步任务、Web 容器创建的新线程里跑的，这些线程的 ContextClassLoader 还是原来的，不是你手动设置的那个。

结果：你以为全局生效了，其实只影响了当前这个线程。

---

## 解决方法

### 让动态类和 EasyExcel 使用“同一个”ClassLoader

思路是：

1. 以 **当前线程的 ContextClassLoader** 作为你自定义 loader 的父类加载器；
2. 用这个自定义 loader 来加载你生成的类；
3. 然后把这个自定义 loader 设置成 ContextClassLoader；
4. 再去调用 EasyExcel 导出。

注意：

- 这段逻辑要确保 **和 EasyExcel 的调用在同一个线程里**；
- `dataList` 里的对象必须真的是 `generatedClass` 的实例，否则会出现各种类型不匹配的问题。

### 1. 自己写一个简单的自定义类加载器

比如新建一个类：`MyDynamicClassLoader`（名字随便起）

```java
public class MyDynamicClassLoader extends ClassLoader {

    // 推荐显式指定 parent，这里用当前线程的 context classloader
    public MyDynamicClassLoader() {
        super(Thread.currentThread().getContextClassLoader());
    }

    public MyDynamicClassLoader(ClassLoader parent) {
        super(parent);
    }

    /**
     * 把一段字节码定义成 Class 对象
     */
    public Class<?> defineClass(String className, byte[] bytes) {
        // 注意：这里直接调用 ClassLoader 自带的 protected defineClass 方法
        return super.defineClass(className, bytes, 0, bytes.length);
    }
}
```

### 2. 和 EasyExcel 配合时，大致用法示例

假设你已经用 ASM 生成了一个类的字节码 `byte[] bytes`，类全名是 `com.example.ExcelModel`：

```java
byte[] bytes = ...; // ASM 生成的字节码
String className = "com.example.ExcelModel";

// 1. 创建自定义 ClassLoader（以当前线程 context classloader 为父）
MyDynamicClassLoader loader =
    new MyDynamicClassLoader(Thread.currentThread().getContextClassLoader());

// 2. 定义类
Class<?> modelClass = loader.defineClass(className, bytes);

// 3. 很关键：把这个 loader 设成当前线程的 ContextClassLoader
ClassLoader old = Thread.currentThread().getContextClassLoader();
Thread.currentThread().setContextClassLoader(loader);
try {
    // 4. 在这个上下文中调用 EasyExcel
    // 下面是示意代码，按你自己的业务来写
    EasyExcel.write(outputStream, modelClass)
             .sheet("sheet1")
             .doWrite(dataList);  // dataList 里的对象类型要和 modelClass 对应
} finally {
    // 5. 恢复原来的 ClassLoader，避免污染其他地方
    Thread.currentThread().setContextClassLoader(old);
}
```

这样做的目的就是让 EasyExcel 内部在解析字段、注解时，用到的 `Thread.currentThread().getContextClassLoader()`  
能“看到”你刚刚动态定义的类，而不至于抛 `NoClassDefFoundError` / `ClassNotFoundException`。

## 一次请求结束后，能不能把这个“动态生成的类”卸载掉？

先把结论说清楚：

- Java 里 **不能单独卸载某一个 Class**。
- **只能在整个 ClassLoader 没有任何强引用、也没有存活对象引用这些类时，JVM 才有机会连同它加载的所有类一起回收**。
- 换句话说：
  - 想卸载类 ⇒ 就得“丢弃这个 ClassLoader” ⇒ 等 GC 把 ClassLoader 和它加载的类一锅端掉。

所以能不能做到“请求完成后自动卸载”，取决于你怎么设计 ClassLoader 的生命周期。

### 方案 A：**每个请求一个 ClassLoader，请求结束后丢弃**

思路：

1. 每次请求：
   1. new 一个 `MyDynamicClassLoader`；
   2. 用它生成/加载本次请求需要的动态类；
   3. 执行业务逻辑、导出 Excel 等；
   4. 请求结束后，不再持有这个 ClassLoader 的任何引用（包括类、实例、缓存等）。
2. 只要：
   - 没有静态字段 / 单例 / 线程本地变量（ThreadLocal）等引用这些类；
   - 没有把动态类的对象放进全局缓存 / 队列 / 线程池等；
3. 那么这个 ClassLoader 和它加载的所有类，**在以后某次 GC 时就会被一起回收，效果等同“卸载”**。

伪代码示例（省略异常处理）：

```java
public void handleRequest() {
    // 1. 为当前请求创建独立的 classloader
    MyDynamicClassLoader loader =
        new MyDynamicClassLoader(Thread.currentThread().getContextClassLoader());

    try {
        // 2. ASM 生成字节码
        byte[] bytes = generateBytesForThisRequest();
        Class<?> modelClass = loader.defineClass("com.demo.DynamicModel", bytes);

        // 3. 用这个 modelClass 做 EasyExcel 导出
        exportExcelWithModel(modelClass);
    } finally {
        // 4. 关键点：不要把 loader / modelClass / 动态对象 存到任何静态变量或全局缓存
        // 只要不再引用，后续 GC 就可以整体回收 loader + 其所有类
    }
}
```

优点：

- 请求结束后，理论上可以被 GC 整体卸载，不会无限堆积类。
- 适合 “每次请求生成的类都不同、且之后不再需要复用” 的场景。

缺点：

- 每次请求新建 ClassLoader 和生成类，**性能开销比较大**；
- 如果你使用了线程池、异步任务，要特别小心：动态类的对象不要“飞出去”到其他线程长期存活。

### 方案 B：**复用一个 ClassLoader + 类缓存，不主动卸载**

思路：

- 如果你生成的动态类是“模板型”的，比如根据配置只会有有限种结构，且会经常复用；
- 那么你可以 **复用一个 `MyDynamicClassLoader`，并缓存已经生成的类**，下次再用就不用重新生成字节码了。

这种方案里，**类是不会被卸载的**（除非整个应用停止 / 热部署卸载），但：

- 类的数量是“有限的”（比如几十个、几百个），不会无限增长；
- 换来的是**更好的性能和更简单的生命周期管理**。

示例：

```java
public class DynamicModelManager {
    private final MyDynamicClassLoader loader =
        new MyDynamicClassLoader(Thread.currentThread().getContextClassLoader());

    private final Map<String, Class<?>> cache = new ConcurrentHashMap<>();

    public Class<?> getOrCreate(String key) {
        return cache.computeIfAbsent(key, k -> {
            byte[] bytes = generateBytesByKey(k);
            return loader.defineClass("com.demo.DynamicModel_" + k, bytes);
        });
    }
}
```
