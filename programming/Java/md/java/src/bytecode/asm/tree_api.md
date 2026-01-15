# Tree API

ASM 默认的用法是“流式 Visitor API”：

- ClassReader.accept(visitor, ...)
- 一边读 class，一边调用 visitXxx，你一边处理一边把东西丢给下游 ClassVisitor/ClassWriter
- 本质上是“边读边写，不保留整棵结构”

而 Tree API 做的是另一套思路：

- 把 class 全部读进来，构造成一个 完整的、可变的对象树，
- 你可以像操作 AST 那样增删改节点，然后再一次性写出去。

## Tree API 的核心类

### ClassNode

实现了 ClassVisitor, 用来承载整个类的信息：

- version
- access
- name
- superName
- interfaces
- fields（`List<FieldNode>`）
- methods（`List<MethodNode>`）
- innerClasses、outerClass、annotations 等

使用方式通常是：

```java
ClassReader cr = new ClassReader(bytes);
ClassNode cn = new ClassNode();
cr.accept(cn, 0);   // 把整个类读进 ClassNode
```

此时 cn 就是完整的类模型，你可以遍历 / 修改里面的 fields、methods 等。

之后再写回：

```java
ClassWriter cw = new ClassWriter(0);
cn.accept(cw);      // 把修改后的 ClassNode 写回
byte[] newBytes = cw.toByteArray();
```

### MethodNode

实现了 MethodVisitor, 一整个方法的信息都在这里：

- access, name, desc, signature, exceptions
- maxStack, maxLocals
- instructions：InsnList（指令链表）
- tryCatchBlocks：`List<TryCatchBlockNode>`
- localVariables：`List<LocalVariableNode>`
- 注解等

你可以直接：

```java
for (MethodNode mn : cn.methods) {
  if (mn.name.equals("foo")) {
    // 在这里疯狂改
  }
}
```

而不是像普通 ASM 那样必须写一堆 visitXxxInsn。

### InsnList + 各种 XxxInsnNode

MethodNode.instructions 是一个 InsnList，内部是一串双向链表节点，节点类型都是 AbstractInsnNode 的子类：

常用的有：

- InsnNode：无操作数指令（如 RETURN, IRETURN, DUP）
- VarInsnNode：局部变量指令（如 ILOAD, ISTORE）
- FieldInsnNode：字段访问（GETFIELD, PUTSTATIC）
- MethodInsnNode：方法调用（INVOKEVIRTUAL, INVOKESTATIC）
- LdcInsnNode：常量加载（LDC "xxx"）
- TypeInsnNode：NEW, CHECKCAST, INSTANCEOF 等
- JumpInsnNode：跳转（IFNE, GOTO）
- LabelNode：标签
- LineNumberNode：行号信息（和调试相关）

操作方式类似链表：

```java
InsnList insns = mn.instructions;

AbstractInsnNode first = insns.getFirst();
AbstractInsnNode last = insns.getLast();

insns.insert(first, newInsn);       // 插到 first 之后
insns.insertBefore(first, newInsn); // 插到 first 之前
insns.add(newInsn);                 // 追加到末尾
insns.remove(someNode);             // 删除某条指令
```

### 其他 Tree Node

- FieldNode：字段信息（名字、类型、初始值、注解）
- AnnotationNode：注解信息
- TryCatchBlockNode：异常处理块
- LocalVariableNode：本地变量调试信息（名称、类型、作用域）

这些都让你能在内存里随意操作类结构，而不用写一堆 visit 方法。

## 适合用 Tree API 的场景

1. 需要复杂的控制流修改
   - 比如：
     - 删除/重排一大段指令
     - 做控制流分析，改跳转目标
     - 在多个位置插入、合并逻辑
2. 要在多次遍历中共享/修改整个类结构
   - 比如先一轮收集信息，再一轮统一改
   - 需要多次 pass，流式 Visitor 不好回头
3. 写原型 / 调试 / 研究现有字节码
   - Tree 结构更直观、好打印、好理解

## 一个小例子

使用 Tree API 给方法开头加打印

```java
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.*;

public class TreeExample implements Opcodes {

  public static byte[] enhance(byte[] origin) throws Exception {
    // 1. 读成 ClassNode
    ClassReader cr = new ClassReader(origin);
    ClassNode cn = new ClassNode();
    cr.accept(cn, 0);

    // 2. 遍历所有方法
    for (MethodNode mn : cn.methods) {
      // 跳过构造函数和静态代码块
      if ("<init>".equals(mn.name) || "<clinit>".equals(mn.name)) {
        continue;
      }

      InsnList insns = new InsnList();

      // System.out.println("enter method: " + mn.name);

      // GETSTATIC java/lang/System.out : Ljava/io/PrintStream;
      insns.add(new FieldInsnNode(
          GETSTATIC,
          "java/lang/System",
          "out",
          "Ljava/io/PrintStream;"
      ));
      // LDC "enter method: xxx"
      insns.add(new LdcInsnNode("enter method: " + mn.name));
      // INVOKEVIRTUAL java/io/PrintStream.println (Ljava/lang/String;)V
      insns.add(new MethodInsnNode(
          INVOKEVIRTUAL,
          "java/io/PrintStream",
          "println",
          "(Ljava/lang/String;)V",
          false
      ));

      // 3. 插入到方法指令开头
      mn.instructions.insert(insns);
    }

    // 4. 写回 ClassWriter
    ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES | ClassWriter.COMPUTE_MAXS);
    cn.accept(cw);
    return cw.toByteArray();
  }
}
```
