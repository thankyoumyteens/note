# 指令集

几乎所有指令都用 Opcodes 常量表示：

- 加载/存储：
  - `ALOAD`, `ILOAD`, `ISTORE`, `ALOAD_0`, `ALOAD_1` 等
- 常量：
  - `ICONST_0` ~ `ICONST_5`, `LDC`
- 方法调用：
  - `INVOKEVIRTUAL`, `INVOKESTATIC`, `INVOKESPECIAL`, `INVOKEINTERFACE`
- 返回：
  - `RETURN`, `IRETURN`, `ARETURN`
- 控制流：
  - `IFNULL`, `IFNONNULL`, `IF_ICMPEQ` 等（先知道有就行）

你会经常写类似的代码：

```java
mv.visitVarInsn(ALOAD, 0);         // 加载 this
mv.visitLdcInsn("hello");          // 压入常量 "hello"
mv.visitMethodInsn(INVOKEVIRTUAL,
    "java/io/PrintStream",
    "println",
    "(Ljava/lang/String;)V",
    false
);
```
