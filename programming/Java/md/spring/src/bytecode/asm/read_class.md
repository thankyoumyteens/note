# 读取 class 内容

通过调用 ClassReader 的 accept 方法, 通过传入自定义的 visitor 来实现解析 class 字节码的功能。常用的 accept 方法:

```java
void accept(ClassVisitor classVisitor, int parsingOptions);
```

- classVisitor: ClassVisitor 是抽象类, 需要传入自定义的 ClassVisitor。accept 方法中会调用 visitField/visitMethod 等方法, 通过重写这些方法, 就可用获得 class 中相应的信息
- parsingOptions 的取值:
  - 0: 读取 class 中的所有信息
  - ClassReader.SKIP_CODE: 跳过代码属性
  - ClassReader.SKIP_DEBUG: 跳过源文件、局部变量表、局部变量类型表、方法参数列表、行号
  - ClassReader.SKIP_FRAME: 跳过帧(visitFrame), 帧是 JVM 验证类阶段使用的数据
  - ClassReader.EXPANDS_FRAMES: 扩展堆栈映射帧

## 依赖

```xml
<dependency>
    <groupId>org.ow2.asm</groupId>
    <artifactId>asm</artifactId>
    <version>9.6</version>
</dependency>
```

## 获取类信息

继承 ClassVisitor, 重写 visit 方法来获取类的信息, 重写 visitAnnotation 方法来获取类的注解信息, 重写 visitField 方法来获取类的字段信息, 重写 visitMethod 方法来获取类的方法信息。

visitField 方法内只会获取字段和方法的基本信息, 如果要获取更多信息, 比如字段上有哪些注解, 就需要写一个自定义类继承 FieldVisitor 并重写它的相关方法, 作为 visitField 方法的返回值。visitMethod 方法同理。

```java
/**
 * 自定义的ClassVisitor, 用来获取类的信息
 */
public class ClassInfoVisitor extends ClassVisitor {
    protected ClassInfoVisitor() {
        super(Opcodes.ASM9);
    }

    /**
     * 获取类的信息
     * classReader.accept方法中会调用
     */
    @Override
    public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
        System.out.println("类名：" + name);
        System.out.println("父类：" + superName);
        if (interfaces != null && interfaces.length > 0) {
            System.out.print("实现的接口：");
            for (String inter : interfaces) {
                System.out.print(inter + " ");
            }
            System.out.println();
        }
    }

    /**
     * 获取类的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        System.out.println("类的注解：" + desc + ", 是否可见：" + visible);
        // 返回自定义的注解Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor();
    }

    /**
     * 获取类的字段信息
     * classReader.accept方法中会调用, 每有一个字段就会调用一次
     */
    @Override
    public FieldVisitor visitField(int access, String name, String desc, String signature, Object value) {
        System.out.println("====================================================================");
        System.out.println("字段名：" + name);
        System.out.println("字段描述符：" + desc);
        System.out.println("字段签名：" + signature);
        if (value != null) {
            System.out.println("static final字段的初始值：" + value);
        }
        // 返回自定义的字段Visitor, 用来获取字段注解
        return new FieldInfoVisitor();
    }

    /**
     * 获取类的方法信息
     * classReader.accept方法中会调用, 每有一个方法就会调用一次
     */
    @Override
    public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
        System.out.println("====================================================================");
        System.out.println("方法名：" + name);
        System.out.println("方法描述符：" + desc);
        System.out.println("方法签名：" + signature);
        if (exceptions != null && exceptions.length > 0) {
            System.out.print("方法手动抛出的异常：");
            for (String exception : exceptions) {
                System.out.print(exception + " ");
            }
            System.out.println();
        }
        // 返回自定义的方法Visitor, 用来获取方法注解, 方法体等信息
        return new MethodInfoVisitor();
    }
}
```

## 获取注解信息

```java
public class AnnotationInfoVisitor extends AnnotationVisitor {

    public AnnotationInfoVisitor() {
        super(Opcodes.ASM9);
    }

    @Override
    public void visit(String name, Object value) {
        // 比如: @Service(value = "demo")
        // name = value
        // value = demo
        System.out.println("注解参数名：" + name + ", 参数值：" + value);
    }
}
```

## 获取字段信息

```java
public class FieldInfoVisitor extends FieldVisitor {

    public FieldInfoVisitor() {
        super(Opcodes.ASM9);
    }

    /**
     * 获取字段的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        System.out.println("字段的注解：" + desc + ", 是否可见：" + visible);
        // 返回自定义字段Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor();
    }
}
```

## 获取方法信息

```java
public class MethodInfoVisitor extends MethodVisitor {

    public MethodInfoVisitor() {
        super(Opcodes.ASM9);
    }

    /**
     * 获取方法的注解信息
     * classReader.accept方法中会调用
     */
    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        System.out.println("方法的注解：" + desc + ", 是否可见：" + visible);
        // 返回自定义字段Visitor, 用来获取注解的参数
        return new AnnotationInfoVisitor();
    }

    @Override
    public void visitCode() {
        super.visitCode();
        System.out.println("方法体开始");
    }

    @Override
    public void visitMaxs(int maxStack, int maxLocals) {
        super.visitMaxs(maxStack, maxLocals);
        System.out.println("方法体结束");
    }

    @Override
    public void visitEnd() {
        super.visitEnd();
        System.out.println("方法结束");
    }

    /**
     * 如果想要获取方法体中的所有指令, 需要重写所有visitXxxInsn方法
     * 此处以visitLdcInsn为例
     * @param value
     */
    @Override
    public void visitLdcInsn(Object value) {
        super.visitLdcInsn(value);
        System.out.println("LDC命令, 参数: " + value);
    }
}
```

## 使用

```java
public static void main(String[] args) throws IOException {
    Path path = FileSystems.getDefault().getPath("");
    path = path.resolve("target/classes/org/example/ReadDemo.class");
    Path absolutePath = path.toAbsolutePath();
    byte[] bytes = Files.readAllBytes(absolutePath);
    ClassReader classReader = new ClassReader(bytes);
    ClassInfoVisitor classInfoVisitor = new ClassInfoVisitor();
    int options = ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES;
    // 传入自定义的visitor
    classReader.accept(classInfoVisitor, options);
    System.out.println("done");
}
```
