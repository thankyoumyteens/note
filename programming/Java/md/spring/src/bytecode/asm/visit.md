# visit 方法

```java
public final void visit(final int version, final int access,
            final String name, final String signature, final String superName,
            final String[] interfaces)
```

参数说明:

- version: 当前类的版本信息, 它的可选取值:
  - Opcodes.V1_5: 使用 Java 5
  - Opcodes.V1_6: 使用 Java 6
  - Opcodes.V1_7: 使用 Java 7
  - Opcodes.V1_8: 使用 Java 8
- access: 当前类的访问标志(access_flags), 它的可选取值:
  - Opcodes.ACC_PUBLIC: 是否为 public 类型
  - Opcodes.ACC_FINAL: 是否被声明为 final, 只有类可设置
  - Opcodes.ACC_SUPER: 是否允许使用 invokevirtual 字节码指令的新语义, JDK1.0.2 之后编译出来的类的这个标志都必须为真
  - Opcodes.ACC_INTERFACE: 标识这是一个接口
  - Opcodes.ACC_ABSTRACT: 是否为 abstract 类型, 对于接口或者抽象类来说, 此标志值为真, 其他类型值为假
  - Opcodes.ACC_SYNTHETIC: 标识这个类并非由用户代码产生的
  - Opcodes.ACC_ANNOTATION: 标识这是一个注解
  - Opcodes.ACC_ENUM: 标识这是一个枚举
  - Opcodes.ACC_MODULE: 标识这是一个模块
- name: 当前类的名称, 比如: org/example/Demo
- signature: 当前类的泛型, 不使用泛型则传入 null
- superName: 当前类的父类, 比如: java/lang/Object
- interfaces: 当前类实现的接口
