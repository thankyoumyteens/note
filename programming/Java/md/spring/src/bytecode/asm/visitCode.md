# visitCode 方法

visitCode 方法用于定义方法体, 它的用法:

```java
// 方法体开始
method.visitCode();

// 字节码指令
method.visitXxxInsn(...);
// ...

// 方法体结束
method.visitMaxs(0, 0);
```
