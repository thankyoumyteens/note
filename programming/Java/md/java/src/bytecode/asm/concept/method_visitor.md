# MethodVisitor

MethodVisitor 是对“单个方法”进行逐字节码级访问/修改的回调对象。也就是说，每个被访问的方法，都会对应一个 MethodVisitor 实例。

## MethodVisitor 的生命周期

1. ClassVisitor.visitMethod(...)
   - 这里你可以决定：
     - 返回一个自定义的 MethodVisitor（要处理/增强这个方法）
     - 返回原始 mv（只转发）
     - 返回 null（跳过这个方法）
2. 在这个 MethodVisitor 上，依次回调这些：
   1. 方法/参数上的注解(可能会有)：
      - visitAnnotation
      - visitParameter
      - visitAttribute
   2. 函数体开始：
      - visitCode()
   3. 一堆“结构信息”：
      - visitFrame（栈帧）
      - visitLabel（标签）
      - visitLineNumber（行号）
      - visitTryCatchBlock（异常块）
   4. 一条一条字节码指令：
      - visitInsn、visitVarInsn、visitMethodInsn、visitFieldInsn、visitJumpInsn、visitLdcInsn、visitIincInsn、visitTableSwitchInsn、visitLookupSwitchInsn ...
   5. 结束前：
      - visitMaxs(maxStack, maxLocals)（如果没开 COMPUTE_MAXS/COMPUTE_FRAMES 需要你自己计算）
   6. 整个方法结束：
      - visitEnd

你在这些回调里可以：

- 观察（做分析、打印日志）
- 修改（丢掉某些指令、改操作数）
- 插入（在特定 label 前后插入新指令）

## MethodVisitor 的核心方法分类

### 方法的信息

```java
// 方法的注解
public AnnotationVisitor visitAnnotation(String descriptor, boolean visible)

// 参数的注解
public AnnotationVisitor visitParameterAnnotation(int parameter, String descriptor, boolean visible)

// 额外属性（一般高级用法）
public void visitAttribute(Attribute attribute)

// 异常处理块：try { ... } catch (Type) { ... }
public void visitTryCatchBlock(Label start, Label end, Label handler, String type)

// 局部变量信息（调试用），不影响逻辑
public void visitLocalVariable(String name, String descriptor, String signature,
                               Label start, Label end, int index)
```

### 代码结构标记

```java
// 标志“代码正式开始”，你想在方法开头插入指令，通常在这里动手（或在第一个 label 前插）
public void visitCode()
// 定义一个跳转标签
public void visitLabel(Label label)
// 源码行号映射（调试用）
public void visitLineNumber(int line, Label start)
// StackMapFrame，JDK 6+ 的校验用
public void visitFrame(int type, int nLocal, Object[] local, int nStack, Object[] stack)
```

### 各种字节码指令（最常用）

#### 零操作数指令

```java
// opcode: 例如 RETURN、IRETURN、ATHROW 等
public void visitInsn(int opcode);
```

#### 访问局部变量

```java
// opcode: 例如 ILOAD、ISTORE 等
// var 就是局部变量槽位编号（0 通常是 this，后面是参数和临时变量）
public void visitVarInsn(int opcode, int var);
```

#### 访问字段

```java
// opcode: 例如 GETFIELD、PUTFIELD、GETSTATIC、PUTSTATIC
// owner：类名（内部名，如 "java/lang/System"）
// descriptor：字段类型描述符，如 "Ljava/lang/String;"、"I" 等
public void visitFieldInsn(int opcode, String owner, String name, String descriptor);
```

#### 调用方法

```java
// opcode: 例如 INVOKEVIRTUAL、INVOKESTATIC、INVOKESPECIAL、INVOKEINTERFACE 等
public void visitMethodInsn(int opcode, String owner, String name,
                            String descriptor, boolean isInterface);
```

#### 加载常量

```java
// 适用于 int / float / long / double / String / Type / Handle 等常量
// 等价于 LDC 指令的效果
public void visitLdcInsn(Object value);
```

#### 跳转与条件分支

```java
// opcode: 例如 IFNULL、IFNONNULL、IFEQ、IFNE、GOTO 等
// label 是跳转目标，用 new Label() 定义，然后在对应位置用 visitLabel(label) 设置标签
public void visitJumpInsn(int opcode, Label label);
```

#### 自增

```java
// 相当于 var += increment
public void visitIincInsn(int var, int increment);
```

#### switch

```java
// 用于连续的 case 值
public void visitTableSwitchInsn(int min, int max, Label dflt, Label... labels);
// 用于离散的 case 值集合
public void visitLookupSwitchInsn(Label dflt, int[] keys, Label[] labels);
```

#### 方法结束

如果 ClassWriter 用了 COMPUTE_MAXS / COMPUTE_FRAMES，这两个你可以写个占位，ASM 会自动修改。否则你得算准确，否则 ClassVerify 直接炸。

```java
public void visitMaxs(int maxStack, int maxLocals);
public void visitEnd();
```
