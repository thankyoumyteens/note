# 限制导出

如果要使模块只能被指定的模块使用, 可以使用 exports 包名 to 模块名, 导出的包只能由 to 之后指定的模块访问, 可以用逗号分隔多个模块名称。

```java
module C {
    // org.example包只能被B模块使用
    exports org.example to A, B;
}
```
