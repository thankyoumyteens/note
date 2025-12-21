# ClassVisitor：类级别访问器（核心抽象）

经典的 访问者模式（Visitor Pattern） 实现，负责在“类级别”上对结构进行访问/修改。

常见重写方法：

```java
public class MyClassVisitor extends ClassVisitor {

    public MyClassVisitor(int api, ClassVisitor cv) {
        super(api, cv);
    }

    @Override
    public void visit(
        int version, int access, String name,
        String signature, String superName, String[] interfaces
    ) {
        // 这里可以修改类名、父类、接口等
        super.visit(version, access, name, signature, superName, interfaces);
    }

    @Override
    public MethodVisitor visitMethod(
        int access, String name, String descriptor,
        String signature, String[] exceptions
    ) {
        // 针对每个方法，你可以返回一个自定义的 MethodVisitor 包装器
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        return new MyMethodVisitor(api, mv, access, name, descriptor);
    }
}
```

关键点：

- 你可以“包一层又一层的 Visitor”，做成责任链
- ClassVisitor 主要负责类、字段、方法的“结构级”操作
- 真正操作方法体（字节码指令），要靠 MethodVisitor
