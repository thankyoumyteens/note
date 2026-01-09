# ClassReader：读取器

ClassReader 的作用：从字节数组 / 输入流中读入 class 文件。

更具体一点：

- 输入：`byte[]` / InputStream / 类名（从 classpath 里找）
- 解析：按 class 文件的格式一点点解析：版本、常量池、类信息、字段、方法、注解、属性等
- 输出：不会直接给你一个“结构体”，而是调用你实现的 XxxVisitor 的方法，比如：
  - visit 类信息
  - visitField 字段信息
  - visitMethod 方法信息
  - visitEnd 访问结束

所以：

- ClassReader 只负责“读 + 解析 + 触发回调”
- 真正的逻辑（打印、修改、过滤、增强）都写在你自己实现的 XxxVisitor 里面

## ClassReader 的常见构造方式

```java
// 1. 直接从字节数组构造
ClassReader cr = new ClassReader(byteArray);

// 2. 从 InputStream
ClassReader cr = new ClassReader(inputStream);

// 3. 从类名（会自己去 classpath 里找 Demo.class）
ClassReader cr = new ClassReader("com.example.Demo");
```

- 从类名构造：
  - 它会用当前线程的 ClassLoader 去找 Demo.class
  - 要求这个类在当前 classpath 里能被找到
  - 适合在“玩 & demo & 小工具”时用，比如：
    ```java
    ClassReader cr = new ClassReader("Demo");
    ```
- 从字节数组构造
  - 这是在 "类加载器里增强字节码" 时最常见的写法：
    ```java
    byte[] originalBytes = ...; // 比如 agent 里拦截到的
    ClassReader cr = new ClassReader(originalBytes);
    ```
- 从 InputStream
  - 比如你自己从 jar 包里解出来的 InputStream：
    ```java
    try (InputStream is = myClassLoader.getResourceAsStream("Demo.class")) {
        ClassReader cr = new ClassReader(is);
    }
    ```

## 核心方法：accept —— “开始遍历”

ClassReader 真正有用的关键方法几乎就一个：

```java
// cv: 你的 ClassVisitor 实现（或者 ClassWriter、或者两者的“链”）
// parsingOptions: 解析选项（很重要，控制解析多少信息）
public void accept(ClassVisitor cv, int parsingOptions)
```

## accept 方法的第二个参数

parsingOptions 是一个位运算标志（可以 | 起来），常用的有：

1. ClassReader.SKIP_DEBUG
   - 含义：跳过调试信息：
     - 行号表（LineNumberTable）
     - 局部变量表（LocalVariableTable）
     - 源码文件名等
   - 适合：
     - 你只想做简单统计、分析，不关心调试信息
     - 想让读取更快一点、占用内存少一点
2. ClassReader.SKIP_CODE
   - 含义：完全不解析方法体里的字节码（Code 属性），你的 MethodVisitor 基本不会收到任何字节码指令相关的回调
   - 适合：
     - 只想看类/字段/方法签名结构，而不关心方法内部实现
     - 比如做类依赖分析、接口扫描等
3. ClassReader.SKIP_FRAMES
   - 含义：不解析 stack map frames（用于验证器、栈帧信息）
   - 这些信息主要用于：
     - 新版 JVM 的字节码验证
     - 像 ClassWriter 的 COMPUTE_FRAMES 会重新计算它
   - 适合：
     - 你不准备自己手工玩 frames
     - 一般配合 ClassWriter.COMPUTE_FRAMES/COMPUTE_MAXS 使用
4. ClassReader.EXPAND_FRAMES
   - 含义：把 stack map frames 转成“完整格式”的帧信息再交给你
   - 对你来说，一般只在你需要自己处理帧时才用
   - 对大部分只做简单插桩的场景：
     - 常见推荐：ClassReader.EXPAND_FRAMES 配合 ClassWriter.COMPUTE_FRAMES

多个标志可以组合使用，比如:

```java
cr.accept(cv, ClassReader.SKIP_DEBUG | ClassReader.EXPAND_FRAMES);
```

## ClassReader 常见的用法

```java
ClassReader cr = new ClassReader(classBytes);
ClassWriter cw = new ClassWriter(cr, ClassWriter.COMPUTE_MAXS);
ClassVisitor cv = new MyClassVisitor(Opcodes.ASM9, cw);

// 开始读取并“把解析到的东西交给” cv
cr.accept(cv, ClassReader.EXPAND_FRAMES);
// 获取 cv 处理后的字节码
byte[] newBytes = cw.toByteArray();
```

整个过程等价于：

1. ClassReader 解析 .class
2. 遇到“类信息”时调用 cv.visit(...)
3. 遇到“字段”时调用 cv.visitField(...)
4. 遇到“方法”时调用 cv.visitMethod(...)
5. 等等
6. 最后调用 cv.visitEnd()

## 一个很简单的示例：统计方法数量

```java
import org.objectweb.asm.*;

public class MethodCountVisitor extends ClassVisitor {
    private int methodCount = 0;
    private String className;

    public MethodCountVisitor(int api) {
        super(api);
    }

    @Override
    public void visit(
            int version,
            int access,
            String name,
            String signature,
            String superName,
            String[] interfaces) {
        this.className = name;
        super.visit(version, access, name, signature, superName, interfaces);
    }

    @Override
    public MethodVisitor visitMethod(
            int access,
            String name,
            String descriptor,
            String signature,
            String[] exceptions) {
        methodCount++;
        return super.visitMethod(access, name, descriptor, signature, exceptions);
    }

    @Override
    public void visitEnd() {
        System.out.println("Class: " + className + ", method count = " + methodCount);
        super.visitEnd();
    }

    public static void main(String[] args) throws Exception {
        // 从类名读取
        ClassReader cr = new ClassReader("Demo");
        ClassVisitor cv = new MethodCountVisitor(Opcodes.ASM9);
        // 仅跳过 debug 信息，加快一点速度
        cr.accept(cv, ClassReader.SKIP_DEBUG);
    }
}
```
