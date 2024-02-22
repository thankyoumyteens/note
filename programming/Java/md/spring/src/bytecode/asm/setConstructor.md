# 设置类的构造器

类的构造器`<init>()`也是使用 visitMethod 方法为添加:

```java
/**
 * 设置类的构造器
 */
private static void setConstructor(ClassWriter writer) {
    // 生成<init>()方法
    MethodVisitor init = writer.visitMethod(Opcodes.ACC_PUBLIC,
            "<init>", "()V", null, null);
    init.visitCode();
    // 调用父类构造器(必须): super();
    init.visitVarInsn(Opcodes.ALOAD, 0);
    init.visitMethodInsn(Opcodes.INVOKESPECIAL,
            "java/lang/Object", "<init>", "()V", false);
    init.visitInsn(Opcodes.RETURN);
    init.visitMaxs(0, 0);
    init.visitEnd();
}
```
