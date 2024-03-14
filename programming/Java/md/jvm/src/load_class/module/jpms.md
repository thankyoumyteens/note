# Java 模块化系统

在 JDK 9 中引入了 Java 模块化系统(Java Platform Module System, JPMS)。在 JDK 9 之前, Java 平台是以 JAR 包的形式发布的, 这些 JAR 包之间没有依赖关系, 可以随意地混用。JDK 9 引入了模块化系统之后, Java 平台被划分为若干个模块, 每个模块有自己的依赖关系和加载顺序。模块化系统使得 Java 平台变得灵活、稳定和易于维护。

在 JDK 9 之前, Java 是通过不同的 package 和 jar 来做功能的区分和隔离的。从 JDK 9 开始, 原有的 Java 标准库已经由一个单一巨大的 rt.jar 分拆成了几十个模块(如 java.base、java.compiler 等模块), 这些模块以.jmod 扩展名标识, 每个模块都包含了一个描述模块的 module-info.class 文件, 这个文件由项目根目录中的源代码文件 module-info.java 编译而来。

java.base 模块比较特殊, 它并不依赖于其他任何模块, 并且 java.base 是其他模块的基础, 所以在其他模块中并不需要显式引用 java.base。

可以使用 java --list-modules 列出 JDK 所有的模块:

```sh
$ java --list-modules
java.base@21.0.2
java.compiler@21.0.2
java.datatransfer@21.0.2
java.desktop@21.0.2
java.instrument@21.0.2
java.logging@21.0.2
java.management@21.0.2
java.management.rmi@21.0.2
java.naming@21.0.2
java.net.http@21.0.2
java.prefs@21.0.2
java.rmi@21.0.2
java.scripting@21.0.2
java.se@21.0.2
java.security.jgss@21.0.2
java.security.sasl@21.0.2
java.smartcardio@21.0.2
java.sql@21.0.2
java.sql.rowset@21.0.2
java.transaction.xa@21.0.2
java.xml@21.0.2
java.xml.crypto@21.0.2
jdk.accessibility@21.0.2
jdk.attach@21.0.2
jdk.charsets@21.0.2
jdk.compiler@21.0.2
jdk.crypto.cryptoki@21.0.2
jdk.crypto.ec@21.0.2
jdk.dynalink@21.0.2
jdk.editpad@21.0.2
jdk.hotspot.agent@21.0.2
jdk.httpserver@21.0.2
jdk.incubator.vector@21.0.2
jdk.internal.ed@21.0.2
jdk.internal.jvmstat@21.0.2
jdk.internal.le@21.0.2
jdk.internal.opt@21.0.2
jdk.internal.vm.ci@21.0.2
jdk.internal.vm.compiler@21.0.2
jdk.internal.vm.compiler.management@21.0.2
jdk.jartool@21.0.2
jdk.javadoc@21.0.2
jdk.jcmd@21.0.2
jdk.jconsole@21.0.2
jdk.jdeps@21.0.2
jdk.jdi@21.0.2
jdk.jdwp.agent@21.0.2
jdk.jfr@21.0.2
jdk.jlink@21.0.2
jdk.jpackage@21.0.2
jdk.jshell@21.0.2
jdk.jsobject@21.0.2
jdk.jstatd@21.0.2
jdk.localedata@21.0.2
jdk.management@21.0.2
jdk.management.agent@21.0.2
jdk.management.jfr@21.0.2
jdk.naming.dns@21.0.2
jdk.naming.rmi@21.0.2
jdk.net@21.0.2
jdk.nio.mapmode@21.0.2
jdk.random@21.0.2
jdk.sctp@21.0.2
jdk.security.auth@21.0.2
jdk.security.jgss@21.0.2
jdk.unsupported@21.0.2
jdk.unsupported.desktop@21.0.2
jdk.xml.dom@21.0.2
jdk.zipfs@21.0.2
```
