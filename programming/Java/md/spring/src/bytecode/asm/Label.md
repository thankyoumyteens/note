# Label

Label 类用来实现分支和循环, 和跳转指令一起使用。通过无参构造方法创建一个 Label, 通过 visitLabel 方法设置 label 表示的位置, 通过 visitJumpInsn 方法跳转到 label 表示的位置。

这段 java 代码:

```java
public void test() {
    if (Math.random() > 0.5) {
        System.out.println("1");
    } else {
        System.out.println("0");
    }
}
```

可以使用下面的 asm 代码实现:

```java
// 给类添加test方法
MethodVisitor test = writer.visitMethod(Opcodes.ACC_PUBLIC, "test", "()V",
        null, null);
// 开始test方法体
test.visitCode();

// 跳转到return语句的label
Label returnMethod = new Label();
// 跳转到System.out.println("0");语句的label
Label print0 = new Label();

// 执行Math.random(), 并把结果入栈
test.visitMethodInsn(Opcodes.INVOKESTATIC, "java/lang/Math",
        "random", "()D", false);
// 向常量池中添加一个double常量0.5, 并把它入栈
test.visitLdcInsn(0.5d);
// 比较 栈顶两个元素: 0.5 和 Math.random()
// 如果 0.5 大于 Math.random(), 会把1入栈
// 如果 0.5 等于 Math.random(), 会把0入栈
// 如果 0.5 小于 Math.random(), 会把-1入栈
test.visitInsn(Opcodes.DCMPL);
// 如果栈顶的值小于0, 则跳转到print0的位置
// 对应java代码: else
test.visitJumpInsn(Opcodes.IFLE, print0);

// 继续执行
// 对应java代码: if (Math.random() > 0.5)

// System.out
test.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System",
        "out", "Ljava/io/PrintStream;");
test.visitLdcInsn("1");
// println
test.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream",
        "println", "(Ljava/lang/String;)V", false);
// 跳转到return
test.visitJumpInsn(Opcodes.GOTO, returnMethod);

// 设置 label: print0 的位置
// visitJumpInsn(Opcodes.IFLE, print0)会跳转到这里
test.visitLabel(print0);
// System.out
test.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System",
        "out", "Ljava/io/PrintStream;");
test.visitLdcInsn("0");
// println
test.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream",
        "println", "(Ljava/lang/String;)V", false);

// 设置 label: returnMethod 的位置
// visitJumpInsn(Opcodes.GOTO, returnMethod)会跳转到这里
test.visitLabel(returnMethod);
// return
test.visitInsn(Opcodes.RETURN);

test.visitMaxs(-1, -1);
test.visitEnd();
```
