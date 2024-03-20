# 读取并修改 class 信息

读取并修改 class 信息与只读取 class 信息类似, 只是需要使用两个参数的构造方法。

## 自定义 ClassVisitor

```java
public class ClassEditor extends ClassVisitor implements Opcodes {

    /**
     * 如果要修改class内容，必须要调用父类的带ClassVisitor参数的构造方法
     *
     * @param api          ASM版本
     * @param classVisitor 传入的ClassVisitor(关键)
     */
    protected ClassEditor(int api, ClassVisitor classVisitor) {
        super(api, classVisitor);
    }

    /**
     * ASM在遍历到当前类的每一个方法时都会调用这个方法
     *
     * @param access     方法的修饰符
     * @param name       方法名
     * @param descriptor 方法描述符
     * @param signature  泛型信息
     * @param exceptions 方法抛出的异常
     * @return 返回一个MethodVisitor，用于访问方法的具体信息
     */
    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        // 修改main方法的方法体
        if (name.equals("main")) {
            // 返回自定义的MethodVisitor, 用于修改方法体
            // 这里我们返回一个匿名内部类
            // 构造方法的第二个参数必传，否则会报错
            return new MethodVisitor(ASM9, mv) {
                @Override
                public void visitCode() {
                    // 在main方法的方法体前面插入一行代码
                    mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out",
                            "Ljava/io/PrintStream;");
                    mv.visitLdcInsn("do something before main method!");
                    mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println"
                            , "(Ljava/lang/String;)V", false);
                    super.visitCode();
                }
            };
        }
        // 其他方法不做修改，直接返回原始的MethodVisitor
        return mv;
    }
}
```

## 使用

```java
ClassReader classReader = new ClassReader(classFileBuffer);
// 用于生成新类
ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS);

ClassEditor classEditor = new ClassEditor(Opcodes.ASM9, classWriter);
classReader.accept(classEditor, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
// 新类的字节码
byte[] new_content classWriter.toByteArray();
```
