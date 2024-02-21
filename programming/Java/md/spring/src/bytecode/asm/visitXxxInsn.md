# 设置方法体

设置方法体的过程:

1. 调用 visitCode 方法标记方法体开始
2. 调用 visitXXXInsn 系列方法设置字节码指令
3. 调用 visitMaxs 方法设置最大栈深度和最大局部变量索引并标记方法体结束

```java
/**
 * 设置方法体
 */
private static void setMethodBody(MethodVisitor methodVisitor) {
    // 方法体开始
    methodVisitor.visitCode();
    // 方法体内容: return Integer.parseInt(param);
    // 把参数放入栈顶
    methodVisitor.visitVarInsn(Opcodes.ALOAD, 1);
    // 调用Integer.parseInt方法,
    // 返回值存放到栈顶
    methodVisitor.visitMethodInsn(
            // INVOKESTATIC指令
            Opcodes.INVOKESTATIC,
            // 方法所在的类
            "java/lang/Integer",
            // 方法名
            "parseInt",
            // 方法描述符
            "(Ljava/lang/String;)I",
            // 是否为接口中定义的方法
            false
    );
    // 返回栈顶的值
    methodVisitor.visitInsn(Opcodes.IRETURN);
    // 方法体结束
    // 由于创建ClassWriter对象时使用了COMPUTE_FRAMES
    // 这里的max_stacks和max_locals设置会被忽略
    methodVisitor.visitMaxs(0, 0);
}
```
