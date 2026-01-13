# asm-commons 里的工具类

最常用的几个工具类

## AdviceAdapter —— 方法增强的“黄金基类”

用途：在方法的“开头/结尾/异常退出”这些关键点插入逻辑，非常适合做：

- 日志：方法入参 / 返回值 / 耗时
- 埋点：方法调用开始/结束上报
- AOP：before / after / around

典型使用方式（在每个方法前后打印日志）：

```java
public class LogMethodVisitor extends AdviceAdapter {

  private final String methodName;

  protected LogMethodVisitor(int api, MethodVisitor mv, int access, String name, String descriptor) {
    super(api, mv, access, name, descriptor);
    this.methodName = name;
  }

  // 方法“真正开始”时回调
  @Override
  protected void onMethodEnter() {
    // 下面的代码等价于: System.out.println("Enter: " + methodName);
    mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
    mv.visitLdcInsn("Enter: " + methodName);
    mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println",
      "(Ljava/lang/String;)V", false);
  }

  // 正常/异常 return 前都会走
  @Override
  protected void onMethodExit(int opcode) {
    // 下面的代码等价于: System.out.println("Exit: " + methodName);
    mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
    mv.visitLdcInsn("Exit: " + methodName);
    mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println",
      "(Ljava/lang/String;)V", false);
  }
}
```

## LocalVariablesSorter —— 自动管理局部变量 slot

用途：

- 你在方法里新增局部变量时，它帮你分配不会冲突的 slot
- 内部会自动更新 maxLocals

平时你自己手动玩 mv.visitVarInsn(ALOAD, index) 之类时，很容易算错 index，尤其是：

- 实例方法有 this
- long / double 占两个 slot
- 你中途插入新变量

典型用法：

```java
// 注意：AdviceAdapter 已经继承了 LocalVariablesSorter，
// 所以如果你用 AdviceAdapter，就不用自己再继承 LocalVariablesSorter 了
public class MyMV extends LocalVariablesSorter {

  protected MyMV(int api, int access, String desc, MethodVisitor mv) {
    super(api, access, desc, mv);
  }

  private int timerIndex;

  @Override
  public void visitCode() {
    super.visitCode();
    // 新增一个 long 局部变量，返回它的 slot
    timerIndex = newLocal(Type.LONG_TYPE);  // 自动分配 index
    mv.visitMethodInsn(INVOKESTATIC, "java/lang/System", "nanoTime", "()J", false);
    mv.visitVarInsn(LSTORE, timerIndex);
  }
}
```

## Method —— 方法描述符的小助手

用途：

- 将 java.lang.reflect.Method 映射成 ASM 的方法描述
- 比直接写 "()V"、"(Ljava/lang/String;I)V" 这种字符串更安全可读
- 配合 GeneratorAdapter 更好用

常用方法：

```java
// 从反射的 Method/Constructor 构造
Method m = Method.getMethod("void foo(String)");

m.getDescriptor();   // ()V, (Ljava/lang/String;)V ...
m.getName();         // foo
m.getReturnType();   // Type
m.getArgumentTypes();// Type[]
```

## GeneratorAdapter —— 用更“Java 味”的方式生成指令

用途：

- 对 MethodVisitor 的一层封装，提供更高级别的 API
- 支持 if / for 这种结构化生成，而不是你自己写 label 和跳转

常见场景：

- 你在生成全新方法时，不想一直写 visitInsn、visitVarInsn 这种底层指令
- 可以写得更像“解释性的 Java 逻辑”

简单例子：

```java
// 生成 int add(int a, int b) { return a + b; }

ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
cw.visit(V1_8, ACC_PUBLIC, "Example", null, "java/lang/Object", null);

// 生成构造器略...

// 1. 方法签名
Method m = Method.getMethod("int add (int, int)");
GeneratorAdapter ga = new GeneratorAdapter(ACC_PUBLIC, m, null, null, cw);

// 2. 方法体
ga.loadArg(0);          // 加载参数 a
ga.loadArg(1);          // 加载参数 b
ga.visitInsn(IADD);     // 相加
ga.returnValue();       // return

ga.endMethod();
cw.visitEnd();

byte[] bytes = cw.toByteArray();
```

## ClassRemapper & Remapper —— 批量重写类/方法/字段名

用途：

- 当你需要重命名类/方法/字段/包时，非常好用
- 典型场景：做字节码混淆、小范围重定位、重写依赖包名等

```java
// 继承 Remapper，实现自己的一套“映射规则”
public class MyRemapper extends Remapper {
  @Override
  public String map(String internalName) {
    // 把类改名
    if (internalName.equals("com/example/OldClass")) {
      return "com/example/NewClass";
    }
    return internalName;
  }
}

// 使用
ClassReader cr = new ClassReader(originalBytes);
ClassWriter cw = new ClassWriter(cr, 0);
// 用 ClassRemapper 包一层 ClassVisitor
ClassVisitor cv = new ClassRemapper(cw, new MyRemapper());
// 让 ClassReader.accept 走进 ClassRemapper，它会自动根据映射规则改名
cr.accept(cv, 0);
byte[] result = cw.toByteArray();
```
