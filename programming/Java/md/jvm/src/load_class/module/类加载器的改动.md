# 类加载器的改动

为了模块化系统的顺利施行，模块化下的类加载器发生了一些变动。

首先，是扩展类加载器被平台类加载器(Platform Class Loader)取代。原来的 rt.jar 和 tools.jar 被拆分成数十个 JMOD 文件，删除了`<JAVA_HOME>\lib\ext`目录，取消了通过 java.ext.dirs 系统变量来扩展 JDK 功能的机制。同时，取消了 jre 目录，因为随时可以组合构建出程序运行所需的 JRE 来，假设用到了 java.base 模块和 java.compiler 模块，那么可以通过以下命令打包出一个 JRE：

```
jlink --module-path $JAVA_HOME/jmods --add-modules java.base,java.compiler --output jre
```

其次，平台类加载器和应用程序类加载器都不再派生自 java.net.URLClassLoader，现在启动类加载器、平台类加载器、应用程序类加载器全都继承于 jdk.internal.loader.BuiltinClassLoader，在 BuiltinClassLoader 中实现了新的模块化架构下类如何从模块中加载的逻辑，以及模块中资源可访问性的处理。

启动类加载器现在是在 Java 虚拟机内部和 Java 类库共同协作实现的类加载器，表示成名为 BootClassLoader 的 Java 类，但为了与之前的代码保持兼容，所有在获取启动类加载器的场景(如 Object.class.getClassLoader())中仍然会返回 null 来代替，而不会得到 BootClassLoader 的实例。

Java 模块化系统规定了三个类加载器负责加载不同的模块，当平台及应用程序类加载器收到类加载请求，在委派给父加载器加载前，要先判断该类是否能够归属到某一个系统模块中，如果可以找到这样的归属关系，就要优先委派给负责那个模块的加载器完成加载。

## 各个类加载器负责的模块

1. 启动类加载器负载加载的模块：
   - java.base
   - java.datatransfer
   - java.desktop
   - java.instrument
   - java.logging
   - java.management
   - java.management.rmi
   - java.naming
   - java.prefs
   - java.rmi
   - java.security.sasl
   - java.xml
   - jdk.httpserver
   - jdk.internal.vm.ci
   - jdk.management
   - jdk.management.agent
   - jdk.naming.rmi
   - jdk.net
   - jdk.sctp
   - jdk.unsupported
2. 平台类加载器负责加载的模块：
   - java.activation
   - java.compiler
   - java.corba
   - java.scripting
   - java.se
   - java.se.ee
   - java.security.jgss
   - java.smartcardio
   - java.sql
   - java.sql.rowset
   - java.transaction
   - java.xml.bind
   - java.xml.crypto
   - java.xml.ws
   - java.xml.ws.annotation
   - jdk.accessibility
   - jdk.charsets
   - jd.crypto.cryptoki
   - jdk.crypto.ec
   - jdk.dynalink
   - jdk.incubator.httpclient
   - jdk.internal.vm.compiler
   - jdk.jsobject
   - jdk.localedata
   - jdk.naming.dns
   - jdk.scripting.nashorn
   - jdk.security.auth
   - jdk.security.jgss
   - jdk.xml.dom
   - jdk.zipfs
3. 应用程序类加载器负载加载的模块
   - jdk.aot
   - jdk.attach
   - jdk.compiler
   - jdk.editpad
   - jdk.hotspot.agent
   - jdk.internal.ed
   - jdk.internal.jvmstat
   - jdk.internal.le
   - jdk.internal.opt
   - jdk.jartool
   - jdk.javadoc
   - jdk.jcmd
   - jdk.jconsole
   - jdk.jdeps
   - jdk.jdi
   - jdk.jdwp.agent
   - jdk.jlink
   - jdk.jshell
   - jdk.jstatd
   - jdk.pack
   - jdk.policytool
   - jdk.rmic
   - jdk.scripting.nashorn.shell
   - jdk.xml.bind
   - jdk.xml.ws
