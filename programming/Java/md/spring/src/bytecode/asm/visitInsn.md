# visitXxxInsn 方法

visitXxxInsn 方法用于执行字节码指令:

- visitInsn(int): 没有操作数的字节码指令, 比如: RETURN
- visitIntInsn(int, int): 有一个 int 操作数的字节码指令, 比如: BIPUSH
- visitVarInsn(int, int): 操作局部变量表的字节码指令, 比如 ILOAD, ISTORE
- visitTypeInsn(int, String): 类/接口相关的字节码指令, 比如 NEW
- visitFieldInsn(int, String, String, String): 操作字段的字节码指令, 比如 PUTFIELD
- visitMethodInsn(int, String, String, String, boolean): 方法调用的字节码指令, 比如 INVOKEVIRTUAL
- visitInvokeDynamicInsn(String, String, Handle, Object...): INVOKEDYNAMIC 指令
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
