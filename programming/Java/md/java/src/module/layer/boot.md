# 引导层

引导层（Boot Layer） 是 JVM 启动时创建的第一个模块层，是整个模块系统的根基。它负责加载和管理 Java 运行时的核心模块（如 java.base、java.lang 等, 也包含了通过 `-m` 或者 `--add-modules` 指定的根模块），并作为所有其他模块层的最终父层。

```java
// 获取引导层
ModuleLayer bootLayer = ModuleLayer.boot();

// 打印引导层包含的模块
bootLayer.modules().forEach(System.out::println);
```

输出:

```sh
java.base
java.logging
java.net.http
java.xml
java.sql
...
```
