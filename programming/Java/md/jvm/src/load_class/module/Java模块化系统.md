# Java模块化系统

在JDK 9中引入了Java模块化系统(Java Platform Module System，JPMS)。在JDK 9之前，Java平台是以JAR包的形式发布的，这些JAR包之间没有依赖关系，可以随意地混用。JDK 9引入了模块化系统之后，Java平台被划分为若干个模块，每个模块有自己的依赖关系和加载顺序。模块化系统使得Java平台变得灵活、稳定和易于维护。

在JDK 9之前，Java是通过不同的package和jar来做功能的区分和隔离的：

![](../img/java_no_module.png)

从JDK 9开始，原有的Java标准库已经由一个单一巨大的rt.jar分拆成了几十个模块(如java.base、java.compiler等模块)，这些模块以.jmod扩展名标识，每个模块都包含了一个描述模块的module-info.class文件，这个文件由项目根目录中的源代码文件module-info.java编译而来。

![](../img/java_module.png)

java.base模块比较特殊，它并不依赖于其他任何模块，并且java.base是其他模块的基础，所以在其他模块中并不需要显式引用java.base。

## 创建模块

创建一个JDK 9模块，只需要创建一个module-info.java文件，并将其放在项目的根目录中：

![](../img/java_module_demo.png)

```java
// service模块的module-info.java
module service {
    // 使用exports声明该模块要对外暴露的包
    exports org.example.service;
}
```

```java
// controller模块的module-info.java
module controller {
    // 使用requires依赖其他模块暴露的包
    requires service;
}
```

## 运行

```
mvn compile
java --module-path controller\target;service\target --module controller/org.example.controller.DemoController
```
