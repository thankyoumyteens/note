# 聚合器模块

有时候，希望使用者只需要依赖一个代表整个库的单个模块就可以快速开发。

实现的方法是使用 transitive 来构建聚合器模块。

聚合器模块不包含代码，它只有一个模块描述符，为所有其他模块设置了依赖的传递：

```java
module libs {
    requires transitive lib1;
    requires transitive lib2;
    requires transitive lib3;
    ...
}
```

JDK 中使用聚合器模块的例子:

```sh
$ java --describe-module java.se
java.se@21.0.2
requires java.compiler transitive
requires java.sql transitive
requires java.management.rmi transitive
requires java.sql.rowset transitive
requires java.instrument transitive
requires java.transaction.xa transitive
requires java.base mandated
requires java.management transitive
requires java.naming transitive
requires java.datatransfer transitive
requires java.xml.crypto transitive
requires java.logging transitive
requires java.net.http transitive
requires java.rmi transitive
requires java.desktop transitive
requires java.xml transitive
requires java.security.jgss transitive
requires java.prefs transitive
requires java.security.sasl transitive
requires java.scripting transitive
```
