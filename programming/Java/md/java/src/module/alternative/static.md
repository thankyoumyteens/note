# 编译时依赖

编译时依赖关系指的是仅在编译期需要的依赖关系。通过将关键字 static 添加到 requires 后面，就可以在模块上表达编译时依赖关系:

```java
module framework1 {
    requires static fastjsonlib;
}
```

- 在编译时, 模块系统会搜索可观察模块的范围(JDK 中的模块和模块路径上的模块)，如果找不到 fastjsonlib 模块，则会抛出错误
- 在运行时，模块系统会忽略 requires static，不会对其进行解析。这意味着，如果一个模块仅通过 requires static 引入，那么在运行时它不会被解析

如果想在运行时解析被 requires static 引入的模块:

1. 方法一, 通过 requires 再引入一次, 注意: 如果 fastjsonlib 被其他某个模块通过 requires 引入, 那么所有对它有编译时依赖的模块都能够读取 fastjsonlib
2. 方法二, 通过 `--add-modules` 把 fastjsonlib 手动添加到模块路径上

编译时依赖的使用场景: 引入编译时注解(比如 lombok、 @Nullable、@NonNull)这种不需要在运行时使用的模块。
