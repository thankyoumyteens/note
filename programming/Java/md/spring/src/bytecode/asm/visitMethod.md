# 为类添加方法

使用 visitMethod 方法为类添加方法:

```java
private static void addMethod(ClassWriter writer) {
    MethodVisitor methodVisitor = writer.visitMethod(
            // 方法的访问标志
            Opcodes.ACC_PUBLIC,
            // 方法名
            "string2int",
            // 方法描述符
            "(Ljava/lang/String;)I",
            // 泛型信息
            null,
            // 抛出的异常
            new String[]{}
    );
    // 设置方法体
    setMethodBody(methodVisitor);
    methodVisitor.visitEnd();
}
```
