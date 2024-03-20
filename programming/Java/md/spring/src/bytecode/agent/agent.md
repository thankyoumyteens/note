# Java Agent

Java agent 是基于 JVMTI 实现，核心部分是 ClassFileLoadHook 和 TransFormClassFile。

ClassFileLoadHook​ 是一个 JVMTI 事件，该事件是 Instrumentation agent 的一个核心事件，主要是在读取字节码文件回调时调用，内部调用了 TransFormClassFile 的函数。

TransFormClassFile​ 的主要作用是调用 java.lang.instrument.ClassFileTransformer 的 tranform​ 方法，该方法由开发者实现，通过 Instrumentation 的 addTransformer 方法进行注册。

在字节码文件加载的时候，会触发 ClassFileLoadHook​ 事件，该事件调用 TransFormClassFile​，通过经由 Instrumentation​ 的 addTransformer 注册的方法完成整体的字节码修改。

对于已加载的类，需要调用 retransformClass​ 函数，然后经由 redefineClasses​ 函数，在读取已加载的字节码文件后，若该字节码文件对应的类关注了 ClassFileLoadHook​ 事件，则调用 ClassFileLoadHook 事件。后续流程与类加载时字节码替换一致。
