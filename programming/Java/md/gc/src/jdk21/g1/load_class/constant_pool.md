# 常量池

JVM 规范规定，虚拟机在创建一个类或接口时，将按照类或接口在 Class 文件中的定义创建相应的常量池(每个类都有一个自己的常量池)。

Class 文件中的 constant_pool 表是常量池的静态描述，虚拟机在对类进行解析和连接之后，将在内存中为该类生成一套运行时常量池。JVM 规范规定，常量池在方法区中进行分配。

| 类型               | JVM 内部的枚举表示              | 说明                       |
| ------------------ | ------------------------------- | -------------------------- |
| Utf8               | JVM_CONSTANT_Utf8               | UTF-8 编码的字符串         |
| Integer            | JVM_CONSTANT_Integer            | 整型字面量                 |
| Float              | JVM_CONSTANT_Float              | 浮点型字面量               |
| Long               | JVM_CONSTANT_Long               | 长整型字面量               |
| Double             | JVM_CONSTANT_Double             | 双精度浮点型字面量         |
| Class              | JVM_CONSTANT_Class              | 类或接口的符号引用         |
| String             | JVM_CONSTANT_String             | 字符串类型字面量           |
| Fieldref           | JVM_CONSTANT_Fieldref           | 字段的符号引用             |
| Methodref          | JVM_CONSTANT_Methodref          | 类中方法的符号引用         |
| InterfaceMethodref | JVM_CONSTANT_InterfaceMethodref | 接口中方法的符号引用       |
| NameAndType        | JVM_CONSTANT_NameAndType        | 字段或方法的部分符号引用   |
| MethodHandle       | JVM_CONSTANT_MethodHandle       | 方法句柄                   |
| MethodType         | JVM_CONSTANT_MethodType         | 方法类型                   |
| Dynamic            | JVM_CONSTANT_Dynamic            | 动态计算常量               |
| InvokeDynamic      | JVM_CONSTANT_InvokeDynamic      | 动态方法调用点             |
| Module             | JVM_CONSTANT_Module             | 模块                       |
| Package            | JVM_CONSTANT_Package            | 一个模块中开放或者导出的包 |

常量池在 HotSpot 内部由 ConstantPool 类型来表示，其数据结构如下:

- 常量池缓存(`_cache`)：持有解释器运行时信息
- 所有者类(`_pool_holder`)：该常量池所在类
- 长度：常量池项的个数
- 类型数组(`_tags`)：描述所有常量池项类型的数组
- 常量池项：描述所有常量池项的数组

## 常量池缓存

如果每次字段或方法的访问都需要解析常量池项的话，将会造成性能下降。为解决这一问题，虚拟机引入了常量池缓存机制。

常量池缓存由一个数组组成，元素类型是常量池缓存项，每个缓存项表示类中引用的一个字段或方法。常量池缓存项有两种类型:

- 字段项：用来支持对类变量和对象的快速访问
- 方法项：用来支持 invoke 系列的函数调用指令，为这些方法调用指令提供快速定位目标方法的能力

实现常量池 Cache 项的数据结构为 ConstantPoolCacheEntry:

```cpp
// --- src/hotspot/share/oops/cpCache.hpp --- //

class ConstantPoolCacheEntry {

 private:
  volatile intx     _indices;  // constant pool index & rewrite bytecodes
  Metadata* volatile   _f1;       // entry specific metadata field
  volatile intx        _f2;       // entry specific int/metadata field
  volatile intx     _flags;    // flags
  // ...
}
```

在函数分发时，对于 invokespecial 和 invokestatic 指令，f2 字段表示目标函数的 methodOop。对于 invokevirtual 指令，若是 final 修饰的函数，f2 字段也直接指向目标函数的 methodOop。

当用到 vtable 时(非 final 的其他 virtual 函数)，f2 字段中则存放目标函数在 vtable 中的索引编号。

在用到 itable 时，虚拟机结合 f1 字段和 f2 字段实现函数分发。对于 invokeinterface 指令，f1 字段指向相应的接口的 klassOop，而 £2 字段中存放的则是方法位于 itable 中的索引编号。虚拟机在执行 invokeinterface 指令时，首先从 f1 字段中得到 klassOop，然后在 itable 的偏移表中，从类实现的接口列表中逐一匹配 klassOop，若匹配失败，说明该类并没有实现该接口，虚拟机将抛出 `java.lang.IncompatibleClassChangeError` 异常。若匹配成功，通过 £2 字段在 itable 的方法表中找到目标方法。
