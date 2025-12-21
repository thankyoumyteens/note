# MethodVisitor：方法内指令访问器

你在这里能做到：

- 读取或插入 局部变量、栈操作、方法调用、分支跳转 等指令

常见方法（只列几个感受下）：

```java
public class MyMethodVisitor extends MethodVisitor {

    public MyMethodVisitor(int api, MethodVisitor mv) {
        super(api, mv);
    }

    @Override
    public void visitCode() {
        // 方法字节码开始
        super.visitCode();
    }

    @Override
    public void visitInsn(int opcode) {
        // 访问无操作数指令，比如 IRETURN, RETURN
        super.visitInsn(opcode);
    }

    @Override
    public void visitMethodInsn(
        int opcode, String owner, String name,
        String descriptor, boolean isInterface
    ) {
        // 访问方法调用指令
        super.visitMethodInsn(opcode, owner, name, descriptor, isInterface);
    }

    @Override
    public void visitMaxs(int maxStack, int maxLocals) {
        // 设置最大栈深度和局部变量个数，一般交给 COMPUTE_FRAMES 自动算
        super.visitMaxs(maxStack, maxLocals);
    }
}
```

常见场景：

- 在方法开头插入一段代码、在 return 前插入日志、在异常块外面加 try-catch 等。
