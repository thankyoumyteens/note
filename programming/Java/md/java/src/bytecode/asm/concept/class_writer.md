# ClassWriter：写回器

作用：把你通过 Visitor 构建/修改的类，重新生成为字节数组。

配套关系：

- ClassReader：读 + 解析已有的 class，走访问者回调
- ClassVisitor / MethodVisitor：你实现逻辑的地方（打印、修改、增强…）
- ClassWriter：收集你在 Visitor 里的修改，最后吐出新的 byte[]，可以直接变成新 .class

典型用法：

```java
ClassReader cr = new ClassReader(originalBytes);
ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS | ClassWriter.COMPUTE_FRAMES);
ClassVisitor cv = new MyClassVisitor(Opcodes.ASM9, cw);
cr.accept(cv, 0);

byte[] newBytes = cw.toByteArray();
```

## ClassWriter 的构造方式

```java
// 1. 不带 ClassReader 的
public ClassWriter(int flags)

// 2. 带 ClassReader 的（更常用）
public ClassWriter(ClassReader classReader, int flags)
```
