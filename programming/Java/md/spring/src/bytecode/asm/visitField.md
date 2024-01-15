# visitField 方法

```java
public final FieldVisitor visitField(final int access, final String name,
            final String desc, final String signature, final Object value)
```

参数说明:

- access: 当前字段的访问标志(access_flags), 它的可选取值:
  - Opcodes.ACC_PUBLIC: 字段是否 public
  - Opcodes.ACC_PRIVATE: 字段是否 private
  - Opcodes.ACC_PROTECTED: 字段是否 protected
  - Opcodes.ACC_STATIC: 字段是否 static
  - Opcodes.ACC_FINAL: 字段是否 final
  - Opcodes.ACC_VOLATILE: 字段是否 volatile
  - Opcodes.ACC_TRANSIENT: 字段是否 transient
  - Opcodes.ACC_SYNTHETIC: 字段是否由编译器自动生成
  - Opcodes.ACC_ENUM: 字段是否 enum
- name: 当前字段的名称
- desc: 当前字段的描述符, 它的可选取值:
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
- signature: 当前字段的泛型, 不使用泛型则传入 null
- value: 当前字段的值, 如果当前字段是一个常量, 就需要传入一个具体的值, 如果当前字段不是常量, 那么可以传入 null
