# ClassVisitor：类级别访问器（核心抽象）

经典的 访问者模式（Visitor Pattern） 实现，负责在“类级别”上对结构进行访问/修改。

ClassReader 负责读 .class，一边读一边调用你实现的 ClassVisitor 的 visitXxx。

你要做的，就是：

- 继承 ClassVisitor
- 重写你关心的那些 visitXXX 方法（类、字段、方法、注解…）
- 想改啥就改，想加啥就加，不管的直接转发给下游。

ClassReader.accept 调用时，整体顺序大致是：

1. visit → 类基本信息
2. visitSource → 源文件信息（可选）
3. visitModule → 模块信息（Java 9+，可选）
4. visitNestHost → Nest 主类（可选）
5. visitOuterClass → 外部类信息（匿名类/内部类场景）
6. 若干注解相关：
   - visitAnnotation
   - visitTypeAnnotation
   - visitAttribute
7. 多次 visitInnerClass（内部类）
8. 多次 visitField （字段）
9. 多次 visitMethod （方法）
10. visitEnd → 结束

## visit —— 类信息

```java
public void visit(
    int version, // class 文件版本（如 Opcodes.V1_8）
    int access, // 访问标志（ACC_PUBLIC, ACC_FINAL, ACC_SUPER 等）
    String name, // 内部类名，形如 "java/lang/String"
    String signature, // 泛型签名（没有就是 null）
    String superName, // 父类内部名（如 java/lang/Object）
    String[] interfaces // 实现的接口名数组
) {
  if (cv != null) {
    cv.visit(version, access, name, signature, superName, interfaces);
  }
}
```

你可以在这里改一些“类级别”的东西，比如：

- 修改类名（注意连带一起处理常量池/引用）
- 修改父类或接口列表
- 改 access 标志（比如加上 ACC_PUBLIC，去掉 ACC_FINAL）

## visitField —— 访问字段

```java
public FieldVisitor visitField(
    int access, // ACC_PRIVATE、ACC_STATIC 等
    String name, // 字段名
    String descriptor, // 字段描述符，如 "I", "Ljava/lang/String;"
    String signature, // 泛型签名
    Object value // 初始值（static final 基本类型常量会有初始值）
) {
  if (cv != null) {
    return cv.visitField(access, name, descriptor, signature, value);
  }
  return null;
}
```

你可以：

- 通过返回 null 来 屏蔽 某些字段（不往下转发）
- 改参数再转发，实现 改名/改 access/改 descriptor
- 包装返回的 FieldVisitor，加注解/属性等

## visitMethod —— 访问方法

```java
public MethodVisitor visitMethod(
    int access, // ACC_PUBLIC, ACC_STATIC, ACC_ABSTRACT 等
    String name, // 方法名
    String descriptor, // 方法描述符，如 "(I)Ljava/lang/String;", "()V"
    String signature, // 泛型签名
    String[] exceptions // 声明抛出的异常列表
) {
  if (cv != null) {
    return cv.visitMethod(access, name, descriptor, signature, exceptions);
  }
  return null;
}
```

这是增强逻辑的核心入口：

- 你可以筛选目标方法（比如只处理某些包下的非抽象实例方法）；
- 返回你自定义的 MethodVisitor 子类，在方法体里插入 / 修改指令。

典型用法:

```java
@Override
public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
  MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
  if (mv == null) return null;

  // 比如为所有非构造方法加日志
  if (!name.equals("<init>") && !name.equals("<clinit>")) {
    // 返回你自定义的 MethodVisitor 子类
    return new MyMethodVisitor(api, mv, name, descriptor);
  }
  return mv;
}
```

## Visitor 链

ClassVisitor 里面几乎所有方法默认实现都是：

```java
if (cv != null) cv.visitXxx(...);
```

这是故意设计成可以链式拼的：

- 最底层通常是 ClassWriter（把访问结果写成字节）
- 上面可以套多层自定义的 ClassVisitor
- 每一层只负责做一件事（单一职责）

示例：

```java
ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
// 最底层是 ClassWriter（把访问结果写成字节）
ClassVisitor cv0 = cw;

// 第一层：打印类名
ClassVisitor cv1 = new PrintClassNameVisitor(Opcodes.ASM9, cv0);

// 第二层：给方法加日志
ClassVisitor cv2 = new AddLogClassVisitor(Opcodes.ASM9, cv1);

ClassReader cr = new ClassReader(bytes);
// 把最顶层的 cv 传给 accept 方法
cr.accept(cv2, 0);
```
