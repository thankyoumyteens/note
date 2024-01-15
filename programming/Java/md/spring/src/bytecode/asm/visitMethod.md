# visitMethod 方法

```java
public final MethodVisitor visitMethod(final int access, final String name,
            final String desc, final String signature, final String[] exceptions)
```

参数说明:

- access: 当前方法的访问标志(access_flags), 它的可选取值:
  - Opcodes.ACC_PUBLIC: 方法是否 public
  - Opcodes.ACC_PRIVATE: 方法是否 private
  - Opcodes.ACC_PROTECTED: 方法是否 protected
  - Opcodes.ACC_STATIC: 方法是否 static
  - Opcodes.ACC_FINAL: 方法是否 final
  - Opcodes.ACC_VOLATILE: 方法是否 volatile
  - Opcodes.ACC_TRANSIENT: 方法是否 transient
  - Opcodes.ACC_SYNTHETIC: 方法是否由编译器自动生成
- name: 当前方法的名称
- desc: 当前方法的描述符, 用描述符来描述方法时, 按照先参数列表、后返回值的顺序描述, 参数列表按照参数的顺序放在一组小括号之内, 比如: ()Ljava/lang/String:
  - B: 基本类型 byte
  - C: 基本类型 char
  - D: 基本类型 double
  - F: 基本类型 float
  - I: 基本类型 int
  - J: 基本类型 long
  - S: 基本类型 short
  - Z: 基本类型 boolean
  - V: 特殊类型 void
  - L: 对象类型, 比如 Ljava/lang/Object;
  - \[: 数组类型, 比如 一维 int 数组: \[I, 二维字符串数组: \[\[Ljava/lang/String;
- signature: 当前方法的泛型, 不使用泛型则传入 null
- exceptions: 如果当前方法抛出异常(throws XxxException), 则需要传入
