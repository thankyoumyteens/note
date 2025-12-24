# ASM 提供的 API

ASM 提供了不同“难度档位”的 API。

## 1. Core API（最原始的 Visitor 写法）

特点：

- 最灵活
- 也是最“硬核”：你手里全是指令 `mv.visitXxx(...)`

适合：

- 已经很熟悉字节码结构，或者需要精细控制指令粒度的场景

## 2. Tree API（ClassNode / MethodNode ...）

把字节码解析成一个 树状结构，类似 AST：

- 你会得到一个 ClassNode
- 里面是 `List<MethodNode>`、`List<FieldNode>`...
- 每个 MethodNode 里面有 InsnList 存放指令节点对象（AbstractInsnNode 子类）

特点：

- 改起来会更直观一点：可以像改一个“指令链表”一样插入/删除
- 最后再“Accept”到 ClassWriter 生成字节数组

适合：

- 逻辑稍复杂的改写、需要整体分析/重排指令的场景

## 3. AdviceAdapter：方法增强的好帮手

这是 ASM 提供的一个 方便做 AOP 的适配器，继承自 MethodVisitor。

它帮你做了很多底层细节，比如：

- 自动给你处理 onMethodEnter()、onMethodExit() 这种钩子
- 自动帮你识别所有返回指令
- 你不需要自己到处判断 IRETURN/ARETURN/LRETURN 等

非常适合：

- 统计方法耗时
- 自动打印入参/出参日志
- 统一 try-catch 包裹等

用法大概是：

```java
public class MyAdviceAdapter extends AdviceAdapter {

    protected MyAdviceAdapter(int api, MethodVisitor mv, int access, String name, String descriptor) {
        super(api, mv, access, name, descriptor);
    }

    @Override
    protected void onMethodEnter() {
        // 方法一进来就执行的字节码
    }

    @Override
    protected void onMethodExit(int opcode) {
        // 不论正常返回还是异常返回，都会走到这里
    }
}
```

## 4. ASMifier：把字节码反推出 ASM 代码

还有一个超好用的工具类：ASMifier

作用：

- 给它一个 .class，它会生成 一段 ASM Java 代码，这段代码执行后，能重新“画”出一模一样的 class。

一般用来“反向学习”：

1. 先写正常 Java 方法
2. 编译
3. 用 ASMifier 生成 ASM 代码
4. 拿来参考：“原来我想要的那段逻辑，这样用 ASM 来写”
