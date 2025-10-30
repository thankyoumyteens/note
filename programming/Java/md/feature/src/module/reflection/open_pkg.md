# 开放指定包的反射权限

```java
module mymodule1 {
    opens com.example.demo;
}
```

一个包可以同时被导出(exports)和开放(opens):

```java
module mymodule1 {
    exports com.example.demo;
    opens com.example.demo;
}
```
