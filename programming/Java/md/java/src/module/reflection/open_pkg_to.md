# 开放指定包的反射权限给指定的模块

```java
module mymodule1 {
    opens com.example.demo to module2;
}
```

此时只有 module2 模块可以反射 com.example.demo 包中的类型。
