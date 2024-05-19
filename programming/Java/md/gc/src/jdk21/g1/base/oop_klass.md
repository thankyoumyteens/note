# Oop-Klass 对象模型

一个 Klass 对象代表一个 Java 类的元数据。oop 指的是 Ordinary Object Pointer(普通对象指针), 它用来指向一个 Java 对象。

## oop

一个 Java 对象分为三个部分: 对象头, 实例数据, 对齐填充。

对象头在 JVM 中使用 oopDesc 类表示:

```cpp
class oopDesc {
  // Mark Word
  // 用于存储对象的运行时记录信息,
  // 如哈希值、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID等
  volatile markOop  _mark;
  // 元数据指针
  // 指向一个存储类的元数据的 Klass 对象
  union _metadata {
    // 未压缩的 Klass 指针
    Klass*      _klass;
    // 压缩的 Klass 指针
    narrowKlass _compressed_klass;
  } _metadata;
};
```

oop 在 JVM 中的层级:

```cpp
//////////////////////////////////////////////
// src/hotspot/share/oops/oopsHierarchy.hpp //
//////////////////////////////////////////////

// 用缩进表示继承关系, oopDesc是下面所有类的父类
//            指向Java对象的指针
typedef class oopDesc* oop;
//              普通Java对象
typedef class   instanceOopDesc* instanceOop;
//              数组对象
typedef class   arrayOopDesc* arrayOop;
//                对象类型的数组
typedef class     objArrayOopDesc* objArrayOop;
//                Java基础数据类型的一维数组
typedef class     typeArrayOopDesc* typeArrayOop;
```

每次 new 一个 Java 对象就时, JVM 就会创建一个新的 oopDesc 对象。

## Klass

Klass 主要提供了两个功能:

1. 用于表示 Java 类。Klass 中保存了一个 Java 类的元数据(类型信息, 包括类名、限定符、常量池、方法字典等)。一个 class 文件被 JVM 加载之后, 就会被解析成一个 Klass 对象存储在内存中
2. 保存虚方法表, 用于实现动态分派

```cpp
//////////////////////////////////////
// src/hotspot/share/oops/klass.hpp //
//////////////////////////////////////

class Klass : public Metadata {
 protected:

  // The "layout helper" is a combined descriptor of object layout.
  // For klasses which are neither instance nor array, the value is zero.
  //
  // For instances, layout helper is a positive number, the instance size.
  // This size is already passed through align_object_size and scaled to bytes.
  // The low order bit is set if instances of this class cannot be
  // allocated using the fastpath.
  //
  // For arrays, layout helper is a negative number, containing four
  // distinct bytes, as follows:
  //    MSB:[tag, hsz, ebt, log2(esz)]:LSB
  // where:
  //    tag is 0x80 if the elements are oops, 0xC0 if non-oops
  //    hsz is array header size in bytes (i.e., offset of first element)
  //    ebt is the BasicType of the elements
  //    esz is the element size in bytes
  // This packed word is arranged so as to be quickly unpacked by the
  // various fast paths that use the various subfields.
  //
  // The esz bits can be used directly by a SLL instruction, without masking.
  //
  // Note that the array-kind tag looks like 0x00 for instance klasses,
  // since their length in bytes is always less than 24Mb.
  //
  // Final note:  This comes first, immediately after C++ vtable,
  // because it is frequently queried.
  jint        _layout_helper;

  // Klass kind used to resolve the runtime type of the instance.
  //  - Used to implement devirtualized oop closure dispatching.
  //  - Various type checking in the JVM
  const KlassKind _kind;

  // Class name.  Instance classes: java/lang/String, etc.  Array classes: [I,
  // [Ljava/lang/String;, etc.  Set to zero for all other kinds of classes.
  Symbol*     _name;

  // java/lang/Class instance mirroring this class
  OopHandle   _java_mirror;

  // Superclass
  Klass*      _super;
  // First subclass (null if none); _subklass->next_sibling() is next one
  Klass* volatile _subklass;
  // Sibling link (or null); links all subklasses of a klass
  Klass* volatile _next_sibling;

  // All klasses loaded by a class loader are chained through these links
  Klass*      _next_link;

  // The VM's representation of the ClassLoader used to load this class.
  // Provide access the corresponding instance java.lang.ClassLoader.
  ClassLoaderData* _class_loader_data;

  int _vtable_len;              // vtable length. This field may be read very often when we
                                // have lots of itable dispatches (e.g., lambdas and streams).
                                // Keep it away from the beginning of a Klass to avoid cacheline
                                // contention that may happen when a nearby object is modified.
  AccessFlags _access_flags;    // Access flags. The class/interface distinction is stored here.
}
```

JVM 中 Klass 的层级:

```cpp
//////////////////////////////////////////////
// src/hotspot/share/oops/oopsHierarchy.hpp //
//////////////////////////////////////////////

// 用缩进表示继承关系, Klass是下面所有类的父类
class Klass;
//      代表一个普通的Java类
class   InstanceKlass;
//        代表java.lang.Class
class     InstanceMirrorKlass;
//        代表java.lang.ClassLoader
class     InstanceClassLoaderKlass;
//        代表java.lang.ref.Reference及其子类
class     InstanceRefKlass;
//      代表数组类型的Java类, 该Java类是JVM内部自动创建的, 由数组维数和数组基础类型唯一确定
class   ArrayKlass;
//        代表对象类型的数组所对应的类, 比如String[].class
class     ObjArrayKlass;
//        代表Java基础数据类型的一维数组所对应的类, 比如int[].class
class     TypeArrayKlass;
```

当 JVM 加载一个 Java 类时, 它会在内部创建一个对应的 Klass 对象, 用来存放该 Java 类的各种信息。而在 Klass 对象创建过程中, 也会计算该 Java 类所创建的 Java 对象需要多大内存空间, 该计算结果会被保存到 Klass 对象中的\_layout_helper 字段中, 这样当运行时需要创建 Java 对象时, 直接根据这个字段的值分配一块内存就好了。

## Handle

Handle 是对 oop 的封装, Handle 的作用:

1. 降低垃圾回收器查找 GC Roots 的复杂度，提高 GC 回收的效率。通过 Handle 可以找到一个 Java 线程拥有的所有 oop
2. 在垃圾回收时, 对象可能会被移动, 如果 oop 的地址发生变化，那么所有的引用都要更新, 当通过 Handle 对 oop 间接引用时，如果 oop 的地址发生变化，那么只需要更新 Handle 中保存的对 oop 的引用即可

```cpp
///////////////////////////////////////////
// src/hotspot/share/runtime/handles.hpp //
///////////////////////////////////////////

class Handle {
 private:
  oop* _handle;
}
```
