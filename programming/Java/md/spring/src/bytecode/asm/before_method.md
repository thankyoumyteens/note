# 在方法前执行

```java
public class ClassEditor extends ClassVisitor implements Opcodes {

    /**
     * ASM在遍历到当前类的每一个方法时都会调用这个方法
     *
     * @param access     方法的修饰符
     * @param name       方法名
     * @param descriptor 方法描述符
     * @param signature  泛型信息
     * @param exceptions 方法抛出的异常
     * @return 返回一个MethodVisitor, 用于访问方法的具体信息
     */
    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        // 修改main方法的方法体
        if (name.equals("main")) {
            // 返回自定义的MethodVisitor, 用于修改方法体
            // 这里我们返回一个匿名内部类
            // 构造方法的第二个参数必传, 否则会报错
            return new MethodVisitor(ASM9, mv) {

                // 在原本的方法前执行
                @Override
                public void visitCode() {
                    // 在main方法的方法体前面插入一行代码
                    mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out",
                            "Ljava/io/PrintStream;");
                    mv.visitLdcInsn("do something before main method!");
                    mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println"
                            , "(Ljava/lang/String;)V", false);
                }
            };
        }
        // 其他方法不做修改, 直接返回原始的MethodVisitor
        return mv;
    }
}
```