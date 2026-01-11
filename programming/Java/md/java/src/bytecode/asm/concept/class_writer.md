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

- 不带 ClassReader 的
  - 适合这两种情况：
    - 从零构造一个全新的类（完全手写类结构）
    - 你很熟悉 max stack / max locals / stack map frames，想手动控制一切（比较硬核）
- 带 ClassReader 的
  - 适合“在已有类上做增强/修改”，而且想用自动计算的一些能力（尤其是 frames）。
  - 这个构造器的特点：
    - ClassWriter 能 访问到原始类的常量池、方法结构 等信息
    - 配合某些 flag（例如 COMPUTE_FRAMES）时，效果更好、更安全

## COMPUTE_MAXS

自动帮你计算每个方法的：

- max_stack：操作数栈最大深度
- max_locals：局部变量表大小

如果你设置了它，你在生成/修改方法时可以对 `visitMaxs(maxStack, maxLocals)` 直接填 0，ASM 会帮你计算：

```java
ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS);
MethodVisitor mv = cw.visitMethod(...);
mv.visitCode();
// ... 你的指令 ...
mv.visitInsn(Opcodes.RETURN);

// 这里可以随便写，ASM 会重新算
mv.visitMaxs(0, 0);
mv.visitEnd();
```

## COMPUTE_FRAMES

自动帮你计算 StackMapFrame（栈映射帧），主要用于 Java 6+ 的校验（尤其是 JDK7+，不算对 frame 直接报错）。

StackMapFrame 是 JVM 验证器用来做字节码类型检查的一堆表，非常繁琐，手写极容易错，一错就：

- VerifyError: Bad type on operand stack
- 或者各种莫名其妙的 java.lang.VerifyError

COMPUTE_FRAMES 开了之后，你就不用自己去写 visitFrame 了，ASM 根据控制流图帮你算。

注意：

- COMPUTE_FRAMES 会多做不少分析，成本比只用 COMPUTE_MAXS 高
- 当你修改控制流（比如插入跳转、try/catch）时，为了避免 frame 错误，一般推荐直接开 COMPUTE_FRAMES

## ClassWriter 里几个重要方法

### visit / visitEnd

定义类的整体信息：

```java
cw.visit(
    version,       // 字节码版本, 比如: Opcodes.V1_8
    access,        // public, final, interface, abstract...
    internalName,  // internal name: com/example/Demo -> "com/example/Demo"
    signature,     // 泛型签名，没有就 null
    superName,     // 父类 internal name
    interfaces     // 实现的接口数组
);
// ...
cw.visitEnd();
```

### visitField

定义字段：

```java
FieldVisitor fv = cw.visitField(
    access, // public, final, interface, abstract...
    name, // 字段名
    descriptor, // 字段描述符, 例如: [Ljava/lang/String; 表示 String[]
    signature, // 泛型签名
    value // 字段值
);
if (fv != null) {
    fv.visitEnd();
}
```

### visitMethod

定义 / 拿到一个方法，并返回 MethodVisitor 让你写指令：

```java
MethodVisitor mv = cw.visitMethod(
    access,
    name,
    descriptor,
    signature,
    exceptions // 声明抛出的异常列表
);
if (mv != null) {
    mv.visitCode();
    // ... 指令 ...
    mv.visitMaxs(0, 0); // 如果开了 COMPUTE_MAXS，可以先写 0,0
    mv.visitEnd();
}
```

## 从零手写一个简单类

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello ASM");
    }
}
```

用 ASM 造出等价的 Hello.class：

```java
import org.objectweb.asm.*;

public class GenerateHello {
    public static byte[] dump() {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES | ClassWriter.COMPUTE_MAXS);

        // public class Hello extends Object {}
        cw.visit(Opcodes.V1_8,
                Opcodes.ACC_PUBLIC,
                "Hello",
                null,
                "java/lang/Object",
                null);

        // 生成默认构造器
        MethodVisitor mv = cw.visitMethod(
                Opcodes.ACC_PUBLIC,
                "<init>",
                "()V",
                null,
                null
        );
        // 默认构造器的方法体
        mv.visitCode();
        mv.visitVarInsn(Opcodes.ALOAD, 0);
        mv.visitMethodInsn(
                Opcodes.INVOKESPECIAL,
                "java/lang/Object",
                "<init>",
                "()V",
                false
        );
        mv.visitInsn(Opcodes.RETURN);
        mv.visitMaxs(0, 0); // 自动算
        mv.visitEnd();

        // 生成 main 方法
        mv = cw.visitMethod(
                Opcodes.ACC_PUBLIC | Opcodes.ACC_STATIC,
                "main",
                "([Ljava/lang/String;)V",
                null,
                null
        );
        // main的方法体
        mv.visitCode();

        // System.out.println("Hello ASM");
        mv.visitFieldInsn(
                Opcodes.GETSTATIC,
                "java/lang/System",
                "out",
                "Ljava/io/PrintStream;"
        );
        mv.visitLdcInsn("Hello ASM");
        mv.visitMethodInsn(
                Opcodes.INVOKEVIRTUAL,
                "java/io/PrintStream",
                "println",
                "(Ljava/lang/String;)V",
                false
        );
        mv.visitInsn(Opcodes.RETURN);

        mv.visitMaxs(0, 0);
        mv.visitEnd();

        cw.visitEnd();

        return cw.toByteArray();
    }

    public static void main(String[] args) throws Exception {
        byte[] bytes = dump();
        java.nio.file.Files.write(java.nio.file.Paths.get("Hello.class"), bytes);
    }
}
```
