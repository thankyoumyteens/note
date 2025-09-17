# 开放反射权限

## 开放整个模块的反射权限

当开放一个模块时，无论是否导出包，模块内的所有类型都可以在运行时被其他模块反射。

只需在模块描述符中添加关键字 open，就可以开放一个模块:

```java
open module mymodule1 {
}
```

## 开放指定包的反射权限

```java
module mymodule1 {
    opens com.example.demo;
}
```

一个包可以同时导出(exports)和开放(opens)。

## 开放指定包的反射权限给指定的模块

```java
module mymodule1 {
    opens com.example.demo to module2;
}
```

此时只有 module2 模块可以反射 com.example.demo 包中的类型。

## 使用命令行选项

有时需要对第三方模块(无法修改源码)进行反射。在这种情况下, 可以使用 java 命令的命令行选项:

```sh
--add-opens 模块/包=目标模块
```

比如

```sh
java --add-opens mymodule1/com.example.demo=module2
```
