# visitXxxInsn 方法

visitXxxInsn 方法用于执行字节码指令:

- visitInsn(int): 没有操作数的字节码指令, 比如: RETURN
- visitIntInsn(int, int): 有一个 int 操作数的字节码指令, 比如: BIPUSH
- visitVarInsn(int, int): 操作局部变量表的字节码指令, 比如 ILOAD, ISTORE
- visitTypeInsn(int, String): 类/接口相关的字节码指令, 比如 NEW
- visitFieldInsn(int, String, String, String): 操作字段的字节码指令, 比如 PUTFIELD
- visitMethodInsn(int, String, String, String, boolean): 方法调用的字节码指令, 比如 INVOKEVIRTUAL
- visitInvokeDynamicInsn(String, String, Handle, Object...): 执行 INVOKEDYNAMIC 指令
- visitJumpInsn(int, Label): 跳转的字节码指令，如 IFEQ

## visitInsn

```java
/**
 * 没有操作数的字节码指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            NOP, ACONST_NULL, ICONST_M1, ICONST_0, ICONST_1,
 *            ICONST_2, ICONST_3, ICONST_4, ICONST_5, LCONST_0, LCONST_1,
 *            FCONST_0, FCONST_1, FCONST_2, DCONST_0, DCONST_1, IALOAD,
 *            LALOAD, FALOAD, DALOAD, AALOAD, BALOAD, CALOAD, SALOAD,
 *            IASTORE, LASTORE, FASTORE, DASTORE, AASTORE, BASTORE, CASTORE,
 *            SASTORE, POP, POP2, DUP, DUP_X1, DUP_X2, DUP2, DUP2_X1,
 *            DUP2_X2, SWAP, IADD, LADD, FADD, DADD, ISUB, LSUB, FSUB, DSUB,
 *            IMUL, LMUL, FMUL, DMUL, IDIV, LDIV, FDIV, DDIV, IREM, LREM,
 *            FREM, DREM, INEG, LNEG, FNEG, DNEG, ISHL, LSHL, ISHR, LSHR,
 *            IUSHR, LUSHR, IAND, LAND, IOR, LOR, IXOR, LXOR, I2L, I2F, I2D,
 *            L2I, L2F, L2D, F2I, F2L, F2D, D2I, D2L, D2F, I2B, I2C, I2S,
 *            LCMP, FCMPL, FCMPG, DCMPL, DCMPG, IRETURN, LRETURN, FRETURN,
 *            DRETURN, ARETURN, RETURN, ARRAYLENGTH, ATHROW, MONITORENTER,
 *            MONITOREXIT
 */
public void visitInsn(int opcode);
```

## visitIntInsn

```java
/**
 * Visits an instruction with a single int operand.
 *
 * @param opcode
 *            opcode可以使用的值:
 *            BIPUSH, SIPUSH, NEWARRAY
 * @param operand
 *            当opcode是BIPUSH时, operand的大小要在[Byte.MIN_VALUE, Byte.MAX_VALUE]以内
 *            当opcode是SIPUSH时, operand的大小要在[Short.MIN_VALUE, Short.MAX_VALUE]以内
 *            当opcode是NEWARRAY时, operand可用的值:
 *                                           Opcodes.T_BOOLEAN, Opcodes.T_CHAR,
 *                                           Opcodes.T_FLOAT, Opcodes.T_DOUBLE,
 *                                           Opcodes.T_BYTE, Opcodes.T_SHORT,
 *                                           Opcodes.T_INT, Opcodes.T_LONG
 */
public void visitIntInsn(int opcode, int operand);
```

## visitVarInsn

```java
/**
 * 操作局部变量表的字节码指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            ILOAD, LLOAD, FLOAD, DLOAD, ALOAD,
 *            ISTORE, LSTORE, FSTORE, DSTORE, ASTORE, RET
 * @param var
 *            var是局部变量表的索引
 */
public void visitVarInsn(int opcode, int var);
```

## visitTypeInsn

```java
/**
 * 类型(类/接口/枚举)相关的字节码指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            NEW, ANEWARRAY, CHECKCAST, INSTANCEOF
 * @param type
 *            类型名, 比如: java/lang/Object
 */
public void visitTypeInsn(int opcode, String type);
```

## visitFieldInsn

```java
/**
 * 操作字段的字节码指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            GETSTATIC, PUTSTATIC, GETFIELD, PUTFIELD
 * @param owner
 *            字段所在的类名, 比如: java/lang/Object
 * @param name
 *            字段名
 * @param desc
 *            字段描述符, 比如: Ljava/lang/String;
 */
public void visitFieldInsn(int opcode, String owner, String name,
        String desc);
```

## visitMethodInsn

```java
/**
 * 方法调用的字节码指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            INVOKEVIRTUAL, INVOKESPECIAL, INVOKESTATIC,
 *            INVOKEINTERFACE
 * @param owner
 *            方法所在的类型名, 比如: java/lang/Object
 * @param name
 *            方法名
 * @param desc
 *            方法描述符, 比如: ()Ljava/lang/String;
 * @param itf
 *            方法所在的类型是否为接口
 */
public void visitMethodInsn(int opcode, String owner, String name,
        String desc, boolean itf);
```

## visitInvokeDynamicInsn

```java
/**
 * 执行INVOKEDYNAMIC指令
 *
 * @param name
 *            方法名
 * @param desc
 *            方法描述符, 比如: ()Ljava/lang/String;
 * @param bsm
 *            引导方法
 * @param bsmArgs
 *            引导方法的参数
 */
public void visitInvokeDynamicInsn(String name, String desc, Handle bsm,
        Object... bsmArgs);
```

## visitJumpInsn

```java
/**
 * 跳转指令
 *
 * @param opcode
 *            opcode可以使用的值:
 *            IFEQ, IFNE, IFLT, IFGE, IFGT, IFLE, IF_ICMPEQ,
 *            IF_ICMPNE, IF_ICMPLT, IF_ICMPGE, IF_ICMPGT, IF_ICMPLE,
 *            IF_ACMPEQ, IF_ACMPNE, GOTO, JSR, IFNULL, IFNONNULL
 * @param label
 *            跳转到的位置
 */
public void visitJumpInsn(int opcode, Label label);
```

## visitLdcInsn

```java
/**
 * 将常量池中的数据入栈
 * LDC系列指令
 *
 * @param cst
 *            常量池中的常量
 */
public void visitLdcInsn(Object cst);
```
