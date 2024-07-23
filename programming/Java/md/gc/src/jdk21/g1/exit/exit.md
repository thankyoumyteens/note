# 退出

一般来说, JVM 有两条退出路径:

1. 虚拟机销毁(destroy vm): 当程序运行到主方法的结尾处, 系统将调用 jni_DestroyJavaVM 函数销毁虚拟机
2. 虚拟机退出(vm exit): 当程序调用 System.exit()函数, 或当 JVM 遇到错误时, JVM 将通过 vm_exit 函数退出

这两条退出途径并不完全相同, 但它们在 Java 层面共享 Shutdown.shutdown 方法, 并在 JVM 层面共享 before_exit 函数和 VM_Exit 操作。
