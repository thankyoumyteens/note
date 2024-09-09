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

为了让 JVM 在判断方法或字段的类型时提高效率，ConstantPoolCacheEntry 中还设计了些状态位字段。为节省空间，这些状态位被设计成共享一个 32 位的字段 flags 中。对于如何区分 ConstantPoolCacheEntry 的类型，便是依靠 flags 字段的一个标志位来确定的:

```cpp
// 字段类型
// bit number |31                                           0|
// _flags     [tos|0|F=1|0|0|0|f|v|0 |0  000 |  field_index  ]
// bit length [ 4 |1| 1 |1|1|1|1|1|1 |1|--3--|------16-------]

// 方法类型
// bit number |31                                           0|
// _flags     [tos|0|F=0|S|A|I|f|0|vf|indy_rf|000|00000|psize]
// bit length [ 4 |1| 1 |1|1|1|1|1|1 |---4---|----8----|--8--]
```

- tos: 描述 TosState。TosState 是栈顶缓存优化技术中的一个术语，它的取值表示栈顶缓存元素的数据类型
- F: 1 表示缓存项类型为字段，0 则表示是缓存项类型为方法
- A: call site 有附加的参数
- I: 通过接口调用的, 必须在 vtable 或 vfinal 中查找
- f: 字段或方法是 final 的
- v: 字段是 volatile 的
- vf: final 修饰的虚方法
- indy_rf: call site 指定的方法解析失败
- field_index: 字段信息的索引
- psize: 方法的参数大小, 只在方法类型的 flags 中存在
