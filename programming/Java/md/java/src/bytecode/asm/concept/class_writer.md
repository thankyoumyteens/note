# ClassWriter：写回器

作用：把你通过 Visitor 构建/修改的类，重新生成为字节数组。

通常的用法：

```java
ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
ClassVisitor cv = new xxxVisitor(Opcodes.ASM9, cw);
// 用 ClassReader 接受 cv
cr.accept(cv, 0);
// 修改后的字节码
byte[] newBytes = cw.toByteArray();
```

你可以理解为：

- ClassWriter 就像一个“录像机”，
- 所有通过 ClassVisitor 发过来的回调（类信息、字段、方法、指令等），
- 它都会“录”下来，最后吐出一个新的 .class 字节数组。
