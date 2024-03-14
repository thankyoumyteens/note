# 模块传递

默认情况下，模块是不可传递的。模块 B 导入了模块 C, 模块 A 又导入了模块 B, 但是 A 不能访问 C 导出的包。

如果需要模块是可传递的, 可以在 requires 关键字后添加 transitive 关键字, 这样 A 就可以访问 C 导出的包了。

```java
module B {
    // 添加关键字 transitive 表示
    // 导入B的模块也会隐式导入C
    requires transitive C;
    exports org.example;
}
```
